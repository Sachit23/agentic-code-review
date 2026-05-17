import logging
import os

import requests


logger = logging.getLogger(__name__)


class GeminiAPIError(RuntimeError):
    pass


def analyze_code(prompt: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise GeminiAPIError("GEMINI_API_KEY is missing. Add it to .env and restart uvicorn.")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, params={"key": api_key}, json=payload, timeout=30)
        result = response.json()
    except requests.RequestException as exc:
        raise GeminiAPIError(f"Gemini request failed: {exc}") from exc
    except ValueError as exc:
        raise GeminiAPIError("Gemini returned a non-JSON response.") from exc

    if response.status_code >= 400:
        error = result.get("error", {})
        message = error.get("message", "Unknown Gemini API error")
        status = error.get("status", response.reason)
        logger.error("Gemini API error: %s (%s)", message, status)
        raise GeminiAPIError(f"{message} ({status})")

    if "candidates" not in result:
        raise GeminiAPIError(f"Gemini response did not include candidates: {result}")

    return result["candidates"][0]["content"]["parts"][0]["text"]
