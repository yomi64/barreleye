import sqlite3
import os
from jellyfin import get_users, get_items
from jellystat import get_watch_events

DB_PATH = os.getenv("DB_PATH", "barreleye.db")

def db_init():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT
        );

        CREATE TABLE IF NOT EXISTS items (
            item_id TEXT PRIMARY KEY,
            name TEXT,
            series_id TEXT,
            series_name TEXT,
            item_type TEXT,
            genres TEXT,
            tags TEXT,
            production_year INTEGER,
            community_rating REAL,
            runtime_ticks INTEGER,
            last_metadata_sync TEXT
        );

        CREATE TABLE IF NOT EXISTS watch_events (
            event_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            item_id TEXT NOT NULL,
            watched_at TEXT NOT NULL,
            playback_duration_sec INTEGER,
            is_paused BOOLEAN
        );

        CREATE INDEX IF NOT EXISTS idx_watch_user ON watch_events(user_id);
        CREATE INDEX IF NOT EXISTS idx_watch_item ON watch_events(item_id);
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)

def sync_users():
    conn = get_connection()
    cursor = conn.cursor()
    users = get_users()
    for user in users:
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, username)
            VALUES (?, ?)
        """, (user["user_id"], user["username"]))
    conn.commit()
    conn.close()

def sync_items():
    conn = get_connection()
    cursor = conn.cursor()
    items = get_items()
    for item in items:
        cursor.execute("""
            INSERT OR IGNORE INTO items (item_id, name, series_id, series_name, item_type, genres, tags, production_year, community_rating, runtime_ticks, last_metadata_sync)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["item_id"],
            item["name"],
            item["series_id"],
            item["series_name"],
            item["item_type"],
            item["genres"],
            item["tags"],
            item["production_year"],
            item["community_rating"],
            item["runtime_ticks"],
            item["last_metadata_sync"]
        ))
    conn.commit()
    conn.close()

def sync_watch_events():
    conn = get_connection()
    cursor = conn.cursor()
    watch_events = get_watch_events()
    for event in watch_events:
        cursor.execute("""
            INSERT OR IGNORE INTO watch_events (event_id, user_id, item_id, watched_at, playback_duration_sec, is_paused)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            event["event_id"],
            event["user_id"],
            event["item_id"],
            event["watched_at"],
            event["playback_duration_sec"],
            event["is_paused"]
        ))
    conn.commit()
    conn.close()