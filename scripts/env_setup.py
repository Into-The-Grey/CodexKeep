# CodexKeep/scripts/env_setup.py

import os
import sys
import psycopg2
from dotenv import load_dotenv
import requests


def load_env_variables():
    """
    Load and validate environment variables from the .env file.
    """
    load_dotenv()
    required_vars = [
        "API_KEY",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "DB_HOST",
        "DB_PORT",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"[ERROR] Missing environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    print("[INFO] Environment variables loaded successfully.")


def connect_to_db():
    """
    Establish a database connection.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        print("[INFO] Database connection successful.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Failed to connect to the database: {e}")
        sys.exit(1)


def test_api_connection():
    """
    Test API connection using the API key.
    """

    api_key = os.getenv("API_KEY")
    headers = {"X-API-Key": api_key}
    try:
        response = requests.get(
            "https://www.bungie.net/Platform/Destiny2/Manifest/", headers=headers, timeout=10
        )
        if response.status_code == 200:
            print("[INFO] Bungie API connection successful.")
            return True
        else:
            print(f"[ERROR] Bungie API returned status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to connect to Bungie API: {e}")
        return False


if __name__ == "__main__":
    load_env_variables()
    db_conn = connect_to_db()
    if not test_api_connection():
        sys.exit(1)
