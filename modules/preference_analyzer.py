# modules/preference_analyzer.py
def run(state):
    """Analyze user preferences into activity tags."""
    interests = state.get("user_input", {}).get("interests", [])
    preferences = []
    if "food" in interests:
        preferences.append("food tour")
    if "nature" in interests:
        preferences.append("park hike")
    if "history" in interests:
        preferences.append("museum visit")
    if "shopping" in interests:
        preferences.append("local market")
    if "nightlife" in interests:
        preferences.append("evening live music")
    state["activity_preferences"] = preferences
    return state
