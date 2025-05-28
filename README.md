# FastAPI Workflow Engine Project

This project provides a pre-configured FastAPI codebase for the workflow engine assignment. The assignment instructions will be delivered via the Wilco platform.

## What's Included

- FastAPI server setup in `main.py`
- Stub task functions: `task_a()`, `task_b()`, `task_c()` in `tasks.py`
- An empty `/workflow` endpoint
- An empty `workflow/` directory for your implementation
- Pre-installed dependencies: FastAPI, uvicorn, pytest

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

## Run the server

```
uvicorn main:app --reload
```

## Run tests

```
pytest
```
