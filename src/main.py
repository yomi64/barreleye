from db import db_init, sync_users, sync_items, sync_watch_events
from tmdb import find_similar

def main():
    db_init()
    sync_users()
    sync_items()
    sync_watch_events()
    similar_movies = find_similar(item_id="f54613933a5ecc0202ecb3d33df743bc", media_type="movie")
    for m in similar_movies:
        print(m["title"], m["release_date"])

if __name__ == "__main__":
    main()