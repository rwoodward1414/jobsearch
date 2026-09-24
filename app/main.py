from contextlib import asynccontextmanager

from fastapi import FastAPI
from agents.job_extractor import extract_job
from db import init_db
from schema.jobdesc_request import JobDescRequest

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/jobdesc")
async def get_job_desc(payload: JobDescRequest):
    print(payload.url)
    return extract_job(payload.url)