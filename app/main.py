from dotenv import load_dotenv
load_dotenv(override=True)

from fastapi import FastAPI, Request
from app.github import comment_on_pr, get_pr_diff
from app.graph import build_graph
from app.llm import GeminiAPIError

app = FastAPI()

graph = build_graph()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    
    if payload.get("action") in ["opened", "synchronize"]:
        print("PR event triggered")
        try:
            process_pr(payload)
        except GeminiAPIError as exc:
            print(f"Skipping AI review: {exc}")
            return {"status": "skipped", "reason": str(exc)}
        except Exception as exc:
            print(f"Failed to process PR webhook: {exc}")
            return {"status": "error", "reason": str(exc)}
        
    return {"status": "ok"}

def process_pr(payload):
    repo = payload["repository"]["full_name"]
    pr_number = payload["number"]
    
    diff = get_pr_diff(repo, pr_number)
    
    result = graph.invoke({
        "diff": diff,
        "security": "",
        "tests": "",
        "refactor": ""
    })
    
    final_comment = f"""
    🔍 **AI Code Review**

    🛡️ Security:
    {result['security']}

    🧪 Tests:
    {result['tests']}

    ♻️ Refactor:
    {result['refactor']}
    """
    
    comment_on_pr(repo, pr_number, final_comment)
