import os
import dotenv
import requests
from db import get_tags, get_genres

dotenv.load_dotenv()

TMDB_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def get_tmdb_genre_map(media_type="movie"):
    """media_type: 'movie' or 'tv'"""
    response = requests.get(
        f"{TMDB_URL}/genre/{media_type}/list",
        params={"api_key": TMDB_API_KEY}
    )
    response.raise_for_status()
    genres = response.json()["genres"]
    genre_map = {}
    for g in genres:
        name = g.get("name")
        gid = g.get("id")
        if name is None or gid is None:
            continue
        genre_map[name.lower()] = gid
    return genre_map

def get_tmdb_keyword_id(tag):
    query = (tag or "").strip()
    if not query:
        return None

    response = requests.get(
        f"{TMDB_URL}/search/keyword",
        params={"api_key": TMDB_API_KEY, "query": query}
    )
    response.raise_for_status()
    results = response.json().get("results", [])

    q_lower = query.lower()
    for r in results:
        name = r.get("name")
        if name and name.lower() == q_lower:
            return r.get("id")
    return results[0].get("id") if results else None

def tags_to_keyword_ids(tags):
    ids = []
    for tag in tags:
        kid = get_tmdb_keyword_id(tag)
        if kid:
            ids.append(kid)
    return ids

def genres_to_genre_ids(genres, genre_map):
    ids = []
    seen = set()
    for g in genres or []:
        if g is None:
            continue
        key = g.strip().lower()
        if not key:
            continue
        gid = genre_map.get(key)
        if gid is None:
            continue
        if gid in seen:
            continue
        ids.append(gid)
        seen.add(gid)
    return ids

def find_similar(item_id, media_type="movie", match_all_genres=False):
    tags = get_tags(item_id)
    genres = get_genres(item_id)

    genre_map = get_tmdb_genre_map(media_type)
    genre_ids = genres_to_genre_ids(genres, genre_map)
    keyword_ids = tags_to_keyword_ids(tags)

    params = {
        "api_key": TMDB_API_KEY,
        "sort_by": "popularity.desc",
    }
    if genre_ids:
        if match_all_genres: 
            seperator = "," 
        else:
            seperator = "|"
        params["with_genres"] = seperator.join(map(str, genre_ids))
    if keyword_ids:
        params["with_keywords"] = "|".join(map(str, keyword_ids))

    response = requests.get(f"{TMDB_URL}/discover/{media_type}", params=params)
    response.raise_for_status()
    return response.json().get("results", [])