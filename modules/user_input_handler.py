# modules/user_input_handler.py
import streamlit as st

def run(context):
    """
    MCP Step: Updates context with weather.
    Reads: context['user_input']
    Writes: context['weather']
    """
    context.validate()
    # ...module logic...
    context.validate()
    return context


