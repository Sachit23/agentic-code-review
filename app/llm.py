import requests, os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def analyze_code(diff):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
    Review this code diff:
    - Find bugs
    - Suggest improvements
    - Identify security issues

    Diff:
    {diff}
    """
    
    payload = {
        "content": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

