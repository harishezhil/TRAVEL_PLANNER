# modules/preference_analyzer.py
from utils.context import Context
def run(context: Context) -> Context:
    """
    MCP Step: Updates context with weather.
    Reads: context['user_input']
    Writes: context['weather']
    """
    context.validate()
    interests = context.get("user_input", {}).get("interests", [])
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
    context["activity_preferences"] = preferences
    context.validate()
    return context
