import requests

def query_gemma(prompt, model="gemma3n:e2b"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()['response'].strip()
    except Exception as e:
        return f"⚠️ Gagal menghubungi model lokal: {e}"
