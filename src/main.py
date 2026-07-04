from db import db_init, sync_users, sync_items, sync_watch_events

def main():
    db_init()
    sync_users()
    sync_items()
    sync_watch_events()

if __name__ == "__main__":
    main()