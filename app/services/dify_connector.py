import requests
import os

DIFY_API_URL = os.getenv("DIFY_API_URL")  # e.g., https://api.dify.ai
DIFY_API_KEY = os.getenv("DIFY_API_KEY")  # from Dify App settings

def call_dify(error_summary: str) -> dict:
    """
    Call the Dify Smart Data Validator workflow.
    Args:
        error_summary (str): Validation errors summary
    Returns:
        dict: Parsed JSON response from Dify workflow
    """
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {
            "query": error_summary
        }
    }

    try:
        resp = requests.post(
            f"{DIFY_API_URL}/v1/workflows/smart-data-validator/run",
            headers=headers,
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()

        # Extract structured output safely
        return data.get("data", {}).get("outputs", {}).get("result", {})
    except Exception as e:
        return {"error": str(e)}
