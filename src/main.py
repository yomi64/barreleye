import dotenv
import os
import requests

dotenv.load_dotenv()

jellyfin_url = os.getenv("JELLYFIN_URL")
jellyfin_api_key = os.getenv("JELLYFIN_API_KEY")

jellystat_url = os.getenv("JELLYSTAT_URL")
jellystat_api_key = os.getenv("JELLYSTAT_API_KEY")

def get_user_id(username):
    url = f"{jellyfin_url}/Users"
    headers = {
        "X-Emby-Token": jellyfin_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        users = response.json()
        for user in users:
            if user['Name'] == username:
                return user['Id']
        print(f"User '{username}' not found.")
        return None
    else:
        print(f"Error fetching users: {response.status_code}")
        return None

def get_user_playback_info(user_id):
    url = f"{jellystat_url}/api/getUserHistory"
    headers = {
        "x-api-token": jellystat_api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={"userid": user_id})
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    if response.status_code == 200:
        return response.json()
    return None

def extract_watch_events(playback_json):
    events = []
    for entry in playback_json.get("results", []):
        completion = entry.get("TranscodingInfo", {}).get("CompletionPercentage")
        events.append({
            "user_id": entry["UserId"],
            "user_name": entry["UserName"],
            "item_id": entry["NowPlayingItemId"],
            "item_name": entry["NowPlayingItemName"],
            "series_name": entry.get("SeriesName"),
            "parent_id": entry.get("ParentId"),
            "watched_at": entry["ActivityDateInserted"],
            "playback_duration_sec": entry["PlaybackDuration"],
            "completion_pct": completion,
        })
    return events

with open("watch_events.json", "w") as f:
    f.write(str(extract_watch_events(get_user_playback_info(get_user_id("Cameron")))))