from fastapi import FastAPI
from agents.job_extractor import extract_job
from schema.jobdesc_request import JobDescRequest

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/jobdesc")
async def get_job_desc(payload: JobDescRequest):
    print(payload.url)
    return extract_job(payload.url)