# modules/destination_data_fetcher.py
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
TICKETMASTER_KEY = os.getenv("TICKETMASTER_API_KEY")

def _get_weather_by_city(city, start_date, end_date):
    """Fetch weather forecast (detailed + summary) for given date range."""
    result_summary = {}
    detailed_forecast = []

    if not OPENWEATHER_KEY:
        return {"error": "Missing OPENWEATHER_API_KEY"}

    try:
        url = (
            f"http://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&appid={OPENWEATHER_KEY}&units=metric"
        )
        resp = requests.get(url, timeout=10).json()

        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        for item in resp.get("list", []):
            dt_txt = item.get("dt_txt")
            if dt_txt:
                date_obj = datetime.strptime(dt_txt.split(" ")[0], "%Y-%m-%d")
                if start_dt <= date_obj <= end_dt:
                    weather_desc = item["weather"][0]["description"]
                    temp = item["main"]["temp"]
                    detailed_forecast.append({
                        "datetime": dt_txt,
                        "temp": temp,
                        "weather": weather_desc
                    })
                    # Build daily summary
                    result_summary.setdefault(date_obj.strftime("%Y-%m-%d"), []).append(weather_desc)

        # Collapse summary per date
        for date_str, conditions in list(result_summary.items()):
            result_summary[date_str] = max(set(conditions), key=conditions.count) if conditions else "N/A"

        return {
            "summary": result_summary,
            "detailed": detailed_forecast
        }

    except Exception as e:
        return {"error": str(e)}


def _get_events_by_city(city, start_date, end_date):
    """Fetch events from Ticketmaster API."""
    events = []
    if not TICKETMASTER_KEY:
        return ["Missing TICKETMASTER_API_KEY"]
    try:
        url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TICKETMASTER_KEY}&city={city}&size=10"
        resp = requests.get(url, timeout=10).json()
        embedded = resp.get("_embedded", {})
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        for ev in embedded.get("events", []):
            name = ev.get("name")
            dates = ev.get("dates", {}).get("start", {})
            local_date = dates.get("localDate")
            if local_date:
                event_dt = datetime.strptime(local_date, "%Y-%m-%d")
                if start_dt <= event_dt <= end_dt:
                    events.append({"name": name, "date": local_date})
            else:
                events.append({"name": name})
    except Exception as e:
        events = [{"error": str(e)}]
    return events


def run(context):
    """
    MCP Step: Updates context with weather.
    Reads: context['user_input']
    Writes: context['weather']
    """
    context.validate()
    user_input = context.get("user_input", {})
    destination = user_input.get("destination", "unknown")
    dates = user_input.get("dates", [])
    start_date = dates[0] if dates else datetime.utcnow().strftime("%Y-%m-%d")
    end_date = dates[1] if len(dates) > 1 else (
        datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=3)
    ).strftime("%Y-%m-%d")

    weather = _get_weather_by_city(destination, start_date, end_date)
    events = _get_events_by_city(destination, start_date, end_date)

    # Simple static fallback for popular places

    popular_places = [f"Top sights in {destination} - search via Places API"]

    context["destination_info"] = {
        "destination": destination,
        "weather": weather,
        "events": events,
        "popular_places": popular_places
    }
    context.validate()
    return context




