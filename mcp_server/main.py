# #mcp_server/main.py
# mcp_server/main.py
import json
from workflow_builder import run_workflow

def process_travel_request(destination, start_date, end_date, budget_level, interests):
    """
    Takes travel details as separate arguments and returns the final workflow state.
    """
    initial_state = {
        "user_input": {
            "destination": destination,
            "dates": [str(start_date), str(end_date)],
            "budget": budget_level,
            "interests": interests
        }
    }
    result = run_workflow(initial_state)
    return result

if __name__ == "__main__":
    # Example standalone run
    sample_request = {
        "destination": "Hyderabad",
        "start_date": "2025/08/12",
        "end_date": "2025/08/12",
        "budget_level": "medium",
        "interests": ["food", "nature"]
    }
    print(json.dumps(
        process_travel_request(
            sample_request["destination"],
            sample_request["start_date"],
            sample_request["end_date"],
            sample_request["budget_level"],
            sample_request["interests"]
        ),
        indent=2
    ))



