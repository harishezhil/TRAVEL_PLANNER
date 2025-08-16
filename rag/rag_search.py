import requests
import os

def search_destinations(state):
    destination = state.get("destination")
    api_key = os.getenv("OPENTRIPMAP_API_KEY")
    if not api_key:
        state["_debug"] = {"error": "Missing OpenTripMap API key"}
        return state

    try:
        # Get coordinates
        geo_url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={destination}&apikey={api_key}"
        coords = requests.get(geo_url).json()
        lat, lon = coords.get("lat"), coords.get("lon")

        # Fetch nearby places
        radius_url = f"https://api.opentripmap.com/0.1/en/places/radius?radius=5000&lon={lon}&lat={lat}&limit=20&apikey={api_key}"
        places_data = requests.get(radius_url).json()

        state["places"] = [
            p["properties"]["name"]
            for p in places_data.get("features", [])
            if p["properties"].get("name")
        ]
    except Exception as e:
        state["_debug"] = {"error": str(e)}

    return state
