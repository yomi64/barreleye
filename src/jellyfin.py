"""
Deals with the Jellyfin API and provides functions to interact with it.
"""

import os
import dotenv
import requests

dotenv.load_dotenv()

jellyfin_url = os.getenv("JELLYFIN_URL")
jellyfin_api_key = os.getenv("JELLYFIN_API_KEY")

def get_users():
    """Fetches all users from the Jellyfin server."""
    results = []
    url = f"{jellyfin_url}/Users"
    headers = {
        "X-Emby-Token": jellyfin_api_key
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
    url = f"{jellyfin_url}/Items"
    headers = {
        "X-Emby-Token": jellyfin_api_key
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