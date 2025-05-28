"""Tests for workflow resilience features."""
import pytest
import asyncio
from datetime import datetime, timedelta
from workflow.resilience import CircuitBreaker, CircuitBreakerOpenError, with_retry

# Helper test functions


async def success_func():
    return "success"


async def fail_func():
    raise ValueError("Simulated failure")


async def fail_then_succeed(fail_count=2):
    """Helper that fails a certain number of times then succeeds."""
    if fail_then_succeed.calls < fail_count:
        fail_then_succeed.calls += 1
        raise ValueError("Simulated failure")
    return "success"
fail_then_succeed.calls = 0


@pytest.fixture(name="circuit_breaker")
def circuit_breaker_fixture() -> CircuitBreaker:
    """Create a circuit breaker instance for testing."""
    return CircuitBreaker(failure_threshold=2, reset_timeout=1)


@pytest.fixture(autouse=True)
def reset_fail_count():
    fail_then_succeed.calls = 0
    yield


@pytest.mark.asyncio
async def test_retry_success():
    """Test that retry logic succeeds after failures."""
    result = await with_retry(
        fail_then_succeed,
        max_retries=3,
        initial_delay=0.1,
        max_delay=1.0,
        kwargs={"fail_count": 2}
    )
    assert result == "success"


@pytest.mark.asyncio
async def test_retry_max_attempts():
    """Test that retry logic fails after max attempts."""
    with pytest.raises(ValueError):
        await with_retry(
            fail_func,
            max_retries=2,
            initial_delay=0.1,
            max_delay=1.0
        )


@pytest.mark.asyncio
async def test_circuit_breaker_opens(circuit_breaker):
    """Test that circuit breaker opens after threshold failures."""
    # Cause failures up to threshold
    for _ in range(2):
        with pytest.raises(ValueError):
            await circuit_breaker.call(fail_func)

    # Circuit should be open now
    with pytest.raises(CircuitBreakerOpenError):
        await circuit_breaker.call(success_func)


@pytest.mark.asyncio
async def test_circuit_breaker_resets(circuit_breaker):
    """Test that circuit breaker resets after timeout."""
    # Open the circuit
    for _ in range(2):
        with pytest.raises(ValueError):
            await circuit_breaker.call(fail_func)

    # Wait for reset timeout
    await asyncio.sleep(1.1)

    # Circuit should allow calls again
    result = await circuit_breaker.call(success_func)
    assert result == "success"


@pytest.mark.asyncio
async def test_retry_with_circuit_breaker(circuit_breaker):
    """Test retry logic working together with circuit breaker."""
    # Should succeed with retries
    result = await with_retry(
        fail_then_succeed,
        max_retries=3,
        initial_delay=0.1,
        max_delay=1.0,
        circuit_breaker=circuit_breaker,
        kwargs={"fail_count": 2}
    )
    assert result == "success"

    # Reset the counter and make it fail more times
    fail_then_succeed.calls = 0

    # Should hit circuit breaker before max retries
    with pytest.raises(CircuitBreakerOpenError):
        await with_retry(
            fail_then_succeed,
            max_retries=5,
            initial_delay=0.1,
            max_delay=1.0,
            circuit_breaker=circuit_breaker,
            kwargs={"fail_count": 4}
        )


@pytest.mark.asyncio
async def test_direct_circuit_breaker():
    """Test circuit breaker class directly."""
    cb = CircuitBreaker(failure_threshold=2, reset_timeout=1)

    # Cause failures up to threshold
    for _ in range(2):
        with pytest.raises(ValueError):
            await cb.call(fail_func)

    # Circuit should be open now
    with pytest.raises(CircuitBreakerOpenError):
        await cb.call(success_func)

    # Wait for reset timeout
    await asyncio.sleep(1.1)

    # Circuit should allow calls again
    result = await cb.call(success_func)
    assert result == "success"
