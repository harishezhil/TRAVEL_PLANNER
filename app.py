# app.py
import streamlit as st
from mcp_server.main import process_travel_request
from datetime import date

st.set_page_config(
    page_title="MCP Travel Planner",
    page_icon="🧳",
    layout="centered"
)

# ---------- HEADER ----------
st.title("🧳 MCP Travel Planner")
st.markdown("Plan your trip with AI-powered recommendations.")

# ---------- TRAVEL FORM ----------
with st.form("travel_form", clear_on_submit=False):
    st.subheader("✈️ Travel Request")

    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination (City)", placeholder="e.g., Hyderabad")
        start_date = st.date_input("Start Date", value=date.today())
    with col2:
        budget_level = st.selectbox("Budget Level", ["low", "medium", "high"])
        end_date = st.date_input("End Date", value=date.today())

    interests = st.multiselect(
        "Interests",
        ["food", "nature", "culture", "shopping", "adventure", "history", "relaxation"],
        default=["food", "nature"]
    )

    submitted = st.form_submit_button("📅 Generate Itinerary")

# ---------- PROCESS & DISPLAY ----------
if submitted:
    if not destination:
        st.warning("Please enter a destination.")
    else:
        with st.spinner("🧠 Thinking... Generating your travel plan..."):
            result = process_travel_request(destination, start_date, end_date, budget_level, interests)
            st.write(result.get("llm_summary", "No RAG data found."))

