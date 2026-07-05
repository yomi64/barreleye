"""
Deals with the Jellyfin API and provides functions to interact with it.
"""

import os
import dotenv
import requests

dotenv.load_dotenv()

JELLYFIN_URL = os.getenv("JELLYFIN_URL")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")

def get_users():
    """Fetches all users from the Jellyfin server."""
    results = []
    url = f"{JELLYFIN_URL}/Users"
    headers = {
        "X-Emby-Token": JELLYFIN_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for user in response.json():
            results.append({
                "user_id": user["Id"],
                "username": user["Name"]
            })
        return results
    else:
        print(f"Error fetching users: {response.status_code}")
        return None

def get_items():
    """Fetches all items from the Jellyfin server."""
    results = []
    url = f"{JELLYFIN_URL}/Items"
    headers = {
        "X-Emby-Token": JELLYFIN_API_KEY
    }
    params = {
        "Recursive": "true",
        "IncludeItemTypes": "Movie,Episode",
        "Fields": "Genres,Tags,ProductionYear,CommunityRating,RunTimeTicks,DateLastMetadataRefresh"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        for item in response.json().get("Items", []):
            results.append({
                "item_id": item["Id"],
                "name": item["Name"],
                "series_id": item.get("SeriesId"),
                "series_name": item.get("SeriesName"),
                "item_type": item["Type"],
                "genres": ",".join(item.get("Genres", [])),
                "tags": ",".join(item.get("Tags", [])),
                "production_year": item.get("ProductionYear"),
                "community_rating": item.get("CommunityRating"),
                "runtime_ticks": item.get("RunTimeTicks"),
                "last_metadata_sync": item.get("DateLastMetadataRefresh")
            })
        return results
    else:
        print(f"Error fetching items: {response.status_code}")
        return None
    
def check_if_avaliable(jellyfin_item_id):
    """Checks if an item is available on the Jellyfin server."""
    url = f"{JELLYFIN_URL}/Items/{jellyfin_item_id}/PlaybackInfo"
    headers = {
        "X-Emby-Token": JELLYFIN_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        print(f"Error checking playback info: {response.status_code}")
        return False

def jellyfin_id_to_tmdb_id(user_id, jellyfin_id):
    """Given a Jellyfin item ID, return its TMDB ID (if present)."""
    url = f"{JELLYFIN_URL}/Users/{user_id}/Items/{jellyfin_id}"
    resp = requests.get(url, headers={"X-Emby-Token": JELLYFIN_API_KEY})
    resp.raise_for_status()
    item = resp.json()
    return item.get("ProviderIds", {}).get("Tmdb")

def tmdb_id_to_jellyfin_id(tmdb_id, user_id, include_item_types: str = "Movie,Series"):
    """
    Given a TMDB ID, search the Jellyfin library and return the matching item ID.
    """
    url = f"{JELLYFIN_URL}/Users/{user_id}/Items"
    params = {
        "Recursive": "true",
        "IncludeItemTypes": include_item_types,
        "Fields": "ProviderIds",
    }
    resp = requests.get(url, headers={"X-Emby-Token": JELLYFIN_API_KEY}, params=params)
    resp.raise_for_status()
    items = resp.json().get("Items", [])
    for item in items:
        if item.get("ProviderIds", {}).get("Tmdb") == str(tmdb_id):
            return item["Id"]
    return None