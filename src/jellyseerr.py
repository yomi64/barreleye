import os
import dotenv
import requests

dotenv.load_dotenv()

JELLYSEERR_URL = os.getenv("JELLYSEERR_URL")
JELLYSEERR_API_KEY = os.getenv("JELLYSEERR_API_KEY")

def request_media(media_id, media_type, seasons=None):
    """
    Submit a request to Jellyseerr.

    media_id: TMDB id of the movie/show
    media_type: "movie" or "tv"
    seasons: list of season numbers to request (only for tv). Use "all" for every season.
    """
    payload = {
        "mediaId": media_id,
        "mediaType": media_type,
    }

    if media_type == "tv":
        payload["seasons"] = seasons if seasons else "all"

    resp = requests.post(
        f"{JELLYSEERR_URL}/api/v1/request",
        json=payload,
        headers={
            "X-Api-Key": JELLYSEERR_API_KEY,
            "Content-Type": "application/json",
        },
    )
    resp.raise_for_status()
    return resp.json()