from fastapi import FastAPI, Request
import json
from app.github import process_pr

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    
    if payload.get("action") in ["opened", "synchronize"]:
        process_pr(payload)
        
    return {"status": "ok"}