import os
import dotenv
import requests

dotenv.load_dotenv()

jellystat_url = os.getenv("JELLYSTAT_URL")
jellystat_api_key = os.getenv("JELLYSTAT_API_KEY")

def get_watch_events():
    """Fetches all watch events from the Jellystat server."""
    results = []
    url = f"{jellystat_url}/stats/getPlaybackActivity"
    headers = {
        "x-api-token": jellystat_api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, json={})
    if response.status_code == 200:
        for event in response.json().get("results", []):
            results.append({
                "event_id": event["Id"],
                "user_id": event["UserId"],
                "item_id": event["NowPlayingItemId"],
                "watched_at": event["ActivityDateInserted"],
                "playback_duration_sec": event["PlaybackDuration"],
                "is_paused": event["IsPaused"]
            })
        return results
    else:
        print(f"Error fetching watch events: {response.status_code}")
        return None