# rag/rag_enricher.py
import os
import json
import requests
from dotenv import load_dotenv
from .prompt_templates import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "gemma2-9b-it")  # Default to a specific Groq model

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def enrich_with_groq(state):
    """Send the itinerary + context to Groq and attach llm_summary to state."""
    try:
        itinerary_json = json.dumps({
            "itinerary": state.get("itinerary_plan"),
            "destination_info": state.get("destination_info"),
            "user_input": state.get("user_input")
        }, indent=2)
    except Exception:
        itinerary_json = "{}"

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(json_data=itinerary_json)}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}" if GROQ_API_KEY else "",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        # attempt to parse JSON
        result = resp.json()
    except Exception as e:
        state["llm_summary"] = f"[Groq request error] {str(e)}"
        return state

    # Debug/logging: store raw response under a debug key for inspection in Streamlit
    state.setdefault("_debug", {})["groq_raw_response"] = result

    # safe extraction: different providers may return different shapes
    if isinstance(result, dict):
        # openai-like shape
        if "choices" in result and result["choices"]:
            # try multiple nested possibilities
            choice = result["choices"][0]
            # OpenAI-style chat: choice['message']['content']
            content = None
            if isinstance(choice, dict):
                if "message" in choice and isinstance(choice["message"], dict):
                    content = choice["message"].get("content")
                elif "text" in choice:
                    content = choice.get("text")
            state["llm_summary"] = content or f"[Groq response present but no content] {choice}"
            return state

        # else: maybe an error shape
        if "error" in result:
            state["llm_summary"] = f"[Groq API error] {result['error']}"
            return state

    # fallback: return entire result as string so user can see what's wrong
    state["llm_summary"] = f"[Unexpected Groq response] {json.dumps(result)[:2000]}"
    return state


