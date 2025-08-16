# modules/itinerary_generator.py
from datetime import datetime, timedelta

def _daterange(start_str, end_str):
    start = datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.strptime(end_str, "%Y-%m-%d")
    days = []
    cur = start
    while cur <= end:
        days.append(cur.strftime("%Y-%m-%d"))
        cur += timedelta(days=1)
    return days

def _suggest_activities(preferences, weather_condition):
    """
    Suggest activities based on preferences + weather.
    """
    prefs = preferences.copy() or ["sightseeing"]

    # If bad weather, lean towards indoor activities
    bad_weather_keywords = ["rain", "storm", "snow", "thunder", "shower"]
    if any(word in weather_condition.lower() for word in bad_weather_keywords):
        indoor_alternatives = ["museum visit", "art gallery", "indoor market", "café hopping"]
        prefs = [act for act in prefs if "indoor" in act.lower()] or indoor_alternatives
    else:
        outdoor_options = ["city walking tour", "park visit", "local food tour", "boat ride"]
        prefs = prefs + [opt for opt in outdoor_options if opt not in prefs]

    return prefs

def run(state):
    user_input = state.get("user_input", {})
    dates = user_input.get("dates", [])
    if not dates:
        state["itinerary_plan"] = {"error": "No dates provided"}
        return state

    start_date, end_date = dates[0], dates[1] if len(dates) > 1 else dates[0]
    days = _daterange(start_date, end_date)

    preferences = state.get("activity_preferences", [])
    destination_info = state.get("destination_info", {})
    destination = destination_info.get("destination", user_input.get("destination", "Unknown"))
    weather_data = destination_info.get("weather", {}).get("summary", {})
    popular_places = destination_info.get("popular_places", [])
    events = destination_info.get("events", [])

    print("DEBUG: user_input =", user_input)
    print("DEBUG: destination =", destination)

    itinerary = {
        "destination": destination,
        "days": []
    }

    for i, date in enumerate(days, start=1):
        weather_condition = weather_data.get(date, "Unknown")
        suggested_activities = _suggest_activities(preferences, weather_condition)
        
        # Match events for the day
        day_events = [e for e in events if e.get("date") == date]

        itinerary["days"].append({
            "date": date,
            "day": i,
            "weather": weather_condition,
            "activities": suggested_activities,
            "suggested_places": popular_places[:3],
            "events": day_events
        })

    # Add budget estimate
    budget_level = user_input.get("budget", "medium")
    budget_map = {"low": 50, "medium": 150, "high": 400}  # per day USD approx
    itinerary["budget_estimate_per_day_usd"] = budget_map.get(budget_level, 150)

    state["itinerary_plan"] = itinerary
    return state



