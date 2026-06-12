from fastapi import FastAPI
from pydantic import BaseModel
from triage import run_triage

app = FastAPI(docs_url="/docs")

class PatientMessage(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Healthcare triage agent is running"}

@app.post("/triage")
def triage(payload: PatientMessage):
    result = run_triage(payload.message)
    return result