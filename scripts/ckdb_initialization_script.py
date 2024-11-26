# CodexKeep Initialization Script with .env Integration
# Purpose: Fetch, batch, and store data from Bungie API to PostgreSQL securely

import requests
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Get sensitive credentials from .env
API_KEY = os.getenv("API_KEY")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# Bungie API Headers
HEADERS = {"X-API-Key": API_KEY}

# ---------------------------
# PHASE 1: Setup and Connection
# ---------------------------


# Establish the PostgreSQL connection
def connect_to_db():
    """
    Test database connection and return the connection object.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("[INFO] Database connection successful")
        return conn
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        exit(1)


# Test the API connection
def test_api_connection():
    """
    Test connection to the Bungie API.
    """
    try:
        response = requests.get(
            "https://www.bungie.net/Platform/Destiny2/Manifest/", headers=HEADERS
        )
        if response.status_code == 200:
            print("[INFO] Bungie API connection successful")
            return True
        else:
            print(f"[ERROR] Bungie API connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to connect to the API: {e}")
        exit(1)


# ---------------------------
# PHASE 2: Error Handling and Logging
# ---------------------------

# Logging setup (could be a file in production)
ERROR_LOG = []


def log_error(error_message):
    """
    Log errors into the ERROR_LOG list for future review.
    """
    print(f"[ERROR] {error_message}")
    ERROR_LOG.append(error_message)


def handle_error(error_message):
    """
    Handle critical errors during execution. Log and decide recovery strategy.
    """
    log_error(error_message)
    # Decide whether to exit or continue based on error type
    print("[INFO] Handling error, attempting recovery...")
    time.sleep(5)


# ---------------------------
# PHASE 3: Data Fetching
# ---------------------------


# Fetch Manifest data
def fetch_manifest():
    """
    Fetch the Manifest from Bungie API.
    """
    try:
        response = requests.get(
            "https://www.bungie.net/Platform/Destiny2/Manifest/", headers=HEADERS
        )
        response.raise_for_status()  # Raise HTTP errors if present
        manifest = response.json()
        return manifest
    except Exception as e:
        handle_error(f"Failed to fetch Manifest: {e}")
        return None


# Fetch Item Definitions
def fetch_item_definitions(manifest):
    """
    Fetch item definitions from the Manifest URLs.
    """
    try:
        item_url = manifest["Response"]["jsonWorldComponentContentPaths"]["en"][
            "DestinyInventoryItemDefinition"
        ]
        full_url = f"https://www.bungie.net{item_url}"
        response = requests.get(full_url, headers=HEADERS)
        response.raise_for_status()
        items = response.json()
        return items
    except Exception as e:
        handle_error(f"Failed to fetch item definitions: {e}")
        return None


# ---------------------------
# PHASE 4: Batch Processing
# ---------------------------

# Batch size and tracking
BATCH_SIZE = 2500
current_batch = []


def process_batch(conn, batch):
    """
    Insert a batch of items into the database and clear memory.
    """
    try:
        cur = conn.cursor()
        for item in batch:
            cur.execute(
                """
                INSERT INTO Items (Name, Description, Rarity, ImageURL)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """,
                (item["name"], item["description"], item["rarity"], item["icon"]),
            )
        conn.commit()
        print(f"[INFO] Successfully processed batch of size {len(batch)}")
    except Exception as e:
        handle_error(f"Failed to process batch: {e}")
    finally:
        current_batch.clear()


def batch_insert(conn, items):
    """
    Batch insert all items into the database.
    """
    count = 0
    for item_id, item_data in items.items():
        current_batch.append(
            {
                "name": item_data["displayProperties"]["name"],
                "description": item_data["displayProperties"]["description"],
                "rarity": item_data["inventory"]["tierTypeName"],
                "icon": f"https://www.bungie.net{item_data['displayProperties']['icon']}",
            }
        )
        count += 1
        if len(current_batch) >= BATCH_SIZE:
            process_batch(conn, current_batch)
            print(f"[INFO] Total items processed: {count}")
    # Process remaining items
    if current_batch:
        process_batch(conn, current_batch)


# ---------------------------
# MAIN EXECUTION
# ---------------------------

if __name__ == "__main__":
    # Phase 1: Setup and Connection
    conn = connect_to_db()
    if not test_api_connection():
        exit(1)

    # Phase 3: Fetch Data
    manifest = fetch_manifest()
    if manifest:
        items = fetch_item_definitions(manifest)
        if items:
            batch_insert(conn, items)

    print("[INFO] Initialization script completed.")
