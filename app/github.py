import requests, os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_pr_diff(repo, pr_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    
    response = requests.get(url, headers=headers)
    #response.raise_for_status()
    return response.text

def comment_on_pr(repo, pr_number, comment):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    
    data = {
        "body": comment
    }
    
    requests.post(url, json=data, headers=headers)