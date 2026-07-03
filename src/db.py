import sqlite3
import os

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
            completion_pct REAL,
            playback_duration_sec INTEGER,
            is_paused BOOLEAN,
            play_method TEXT
        );

        CREATE INDEX IF NOT EXISTS idx_watch_user ON watch_events(user_id);
        CREATE INDEX IF NOT EXISTS idx_watch_item ON watch_events(item_id);
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)