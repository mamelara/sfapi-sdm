import requests
import os
import json

from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import PrivateKeyJWT
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Job(BaseModel):
    name: str
    queue: str
    submission_script: str


TOKEN_URL = "https://oidc.nersc.gov/c2id/token"
CLIENT_ID = os.getenv("CLIENT_ID")
PRIVATE_KEY = json.loads(os.getenv("PRIVATE_KEY"))

session = OAuth2Session(
    CLIENT_ID,
    PRIVATE_KEY,
    PrivateKeyJWT(TOKEN_URL),
    grant_type="client_credentials",
    token_endpoint=TOKEN_URL
)

session.fetch_token()

app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'Super facility API job submission test'}


@app.get("/status/")
async def status():
    system = "cori"
    r = session.get("https://api.nersc.gov/api/v1.2/status/" + system)
    cori_status = r.json()
    return cori_status


@app.post("/job/")
async def create_job(job: Job):
    system = "cori"
    submit_script = "/global/cfs/cdirs/seqfs/scratch/jobs/mergill0y7OmNk/script.sh"
    r = session.post("https://api.nersc.gov/api/v1.2/compute/jobs/" + system,
                     data= {"job": submit_script, "isPath": True})
    return r.json()


@app.get("/job/{job_id}")
async def get_job_status(job_id: int):
    machine="cori"
    r = session.get(f"https://api.nersc.gov/api/v1.2/compute/jobs/{machine}/{job_id}?sacct=true")
    return r.json()