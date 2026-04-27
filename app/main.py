from fastapi import FastAPI, Request
import json
from app.github import comment_on_pr, process_pr, get_pr_diff
from analyzer import run_analysis

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    
    if payload.get("action") in ["opened", "synchronize"]:
        process_pr(payload)
        
    return {"status": "ok"}

def process_pr(payload):
    repo = payload["repository"]["full_name"]
    pr_number = payload["number"]
    
    diff = get_pr_diff(repo, pr_number)
    analysis = run_analysis(diff)
    
    comment_on_pr(repo, pr_number, analysis)