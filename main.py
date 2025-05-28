from fastapi import FastAPI
from redis import Redis
from fastapi.responses import JSONResponse

app = FastAPI()
redis_client = Redis(host='localhost', port=6379, db=0)


@app.get("/")
def root():
    return JSONResponse({
        "status": "success",
        "message": "Welcome to the FastAPI application!",
    })


@app.get("/workflow")
def workflow():
    return {}
