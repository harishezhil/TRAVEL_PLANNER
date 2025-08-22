# workflow_builder.py
import logging
from datetime import datetime
from utils.context import Context
from modules import user_input_handler, destination_data_fetcher, preference_analyzer, itinerary_generator
from rag.rag_enricher import enrich_with_groq
from rag.rag_search import search_destinations  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MCPApp")

def run_workflow(initial_state):
    state = Context(initial_state)
    state["mcp_version"] = "1.0"
    state["model_info"] = {"provider": "groq", "model": "llama3"}
    state["history"] = []

    steps = [
        ("UserInputHandler", user_input_handler.run),
        ("DestinationDataFetcher", destination_data_fetcher.run),
        ("RAGSearch", search_destinations),
        ("PreferenceAnalyzer", preference_analyzer.run),
        ("ItineraryGenerator", itinerary_generator.run),
        ("RAGEnrichment", enrich_with_groq),
    ]

    logger.info(f"Starting workflow with {len(steps)} steps...")
    for step_name, step_func in steps:
        logger.info(f"Running step: {step_name}")
        state = step_func(state)
        logger.info(f"State after {step_name}: keys={list(state.keys())}")
        state["history"].append({
            "step": step_name,
            "timestamp": datetime.utcnow().isoformat(),
            "keys": list(state.keys())
        })
        state.validate()

    state["feedback"] = {}
    logger.info("Workflow finished.")
    return state

