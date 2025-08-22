import requests
import os

DIFY_API_URL = os.getenv("DIFY_API_URL")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

def call_dify(query: str) -> str:
    headers = {"Authorization": f"Bearer {DIFY_API_KEY}"}
    payload = {"inputs": {"query": query}}
    resp = requests.post(f"{DIFY_API_URL}/v1/workflows/run", headers=headers, json=payload)
    return resp.json()
