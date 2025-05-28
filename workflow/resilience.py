"""Resilience features for the workflow engine."""
import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class CircuitBreaker:
    """Circuit breaker implementation."""

    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
        """Initialize circuit breaker.

        Args:
            failure_threshold: Number of consecutive failures before opening circuit
            reset_timeout: Seconds to wait before attempting to close circuit
        """
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure_time: Optional[datetime] = None
        self.is_open = False

    async def call(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if self.is_open:
            if self.last_failure_time and \
               datetime.now() - self.last_failure_time > timedelta(seconds=self.reset_timeout):
                # Try to close the circuit
                self.is_open = False
                self.failures = 0
            else:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker is open. Try again in {self.reset_timeout} seconds")

        try:
            result = await func(*args, **kwargs)
            # Success - reset failure count
            self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = datetime.now()
            if self.failures >= self.failure_threshold:
                self.is_open = True
                logger.warning(
                    f"Circuit breaker opened after {self.failures} failures")
            raise e


class CircuitBreakerOpenError(Exception):
    """Raised when attempting to call through an open circuit."""
    pass


async def with_retry(
    func: Callable[..., Any],
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    circuit_breaker: Optional[CircuitBreaker] = None,
    args: tuple = (),
    kwargs: Dict[str, Any] = None,
) -> Any:
    """Execute a function with retry logic and optional circuit breaker.

    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        exponential_base: Base for exponential backoff calculation
        circuit_breaker: Optional circuit breaker instance
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        The result of the function call

    Raises:
        Exception: The last exception encountered after all retries
    """
    last_exception = None
    delay = initial_delay

    kwargs = kwargs or {}

    for attempt in range(max_retries + 1):
        try:
            if circuit_breaker:
                return await circuit_breaker.call(func, *args, **kwargs)
            return await func(*args, **kwargs)

        except Exception as e:
            last_exception = e
            if attempt == max_retries:
                logger.error(f"Final retry attempt failed: {str(e)}")
                raise last_exception

            # Calculate next delay with exponential backoff
            delay = min(delay * exponential_base, max_delay)
            jitter = delay * 0.1  # Add 10% jitter
            actual_delay = delay + (jitter * (random.random() - 0.5))

            logger.warning(
                f"Attempt {attempt + 1}/{max_retries + 1} failed: {str(e)}. "
                f"Retrying in {actual_delay:.2f} seconds..."
            )
            await asyncio.sleep(actual_delay)
