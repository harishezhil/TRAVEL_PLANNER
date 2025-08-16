# modules/user_input_handler.py
import streamlit as st

def run(state):
    """Pass-through or CLI fallback for user input."""
    if "user_input" not in state:
        state["user_input"] = {
            "destination": "",
            "dates": ["", ""],
            "budget": "",
            "interests": []
        }
    return state


