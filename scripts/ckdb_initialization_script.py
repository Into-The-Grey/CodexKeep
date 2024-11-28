# CodexKeep Initialization Script with .env Integration
# Purpose: Fetch, batch, and store data from Bungie API to PostgreSQL securely

import os
import sys
import time
import traceback
import requests
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

# Load environment variables
load_dotenv()

# Get sensitive credentials from .env
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("[ERROR] Missing required environment variables: API_KEY")
    sys.exit(1)
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# Bungie API Headers
HEADERS = {"X-API-Key": API_KEY}

# CodexKeep Initialization Script - Phase 1: Setup and Connection
# Purpose: Initialize API and database connections, validate configurations, and prepare for data operations


# ---------------------------
# STEP 1: Load Environment Variables
# ---------------------------


def load_env_variables():
    """
    Load and validate environment variables from the .env file.
    """
    load_dotenv()

    # Required environment variables
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
        print(
            f"[ERROR] Missing required environment variables: {', '.join(missing_vars)}"
        )
        sys.exit(1)

    print("[INFO] Environment variables successfully loaded and validated.")


# ---------------------------
# STEP 2: Initialize Database Connection
# ---------------------------


def connect_to_db():
    """
    Test database connection and return the connection object.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        print("[INFO] Database connection successful")
        return conn
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Failed to connect to the database: {e}")
        sys.exit(1)


# ---------------------------
# STEP 3: Test API Connection
# ---------------------------


def test_api_connection():
    """
    Test connection to the Bungie API and validate API key.
    """
    headers = {"X-API-Key": API_KEY}

    try:
        response = requests.get(
            "https://www.bungie.net/Platform/Destiny2/Manifest/",
            headers=headers,
            timeout=10,
        )
        if response.status_code == 200:
            print("[INFO] Bungie API connection successful")
            return True
        elif response.status_code == 401:
            print("[ERROR] Invalid API key. Please check your .env file.")
        else:
            print(f"[ERROR] Bungie API returned status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to connect to the Bungie API: {e}")
    return False


# ---------------------------
# STEP 4: Initialize and Test Everything
# ---------------------------


def handle_critical_error(error_message, exit_on_failure=False):
    """
    Handle an error by logging it and deciding whether to proceed or exit.
    :param error_message: A description of the error.
    :param exit_on_failure: Whether the script should terminate after this error (default: False).
    """
    log_error(error_message)

    if exit_on_failure:
        print("[INFO] Terminating script due to critical error.")
        sys.exit(1)  # Exit with failure status
    else:
        print("[INFO] Attempting to recover from error...")
        time.sleep(3)  # Optional recovery delay


def initialize_connections():
    """
    Load environment variables, initialize database and API connections.
    """
    print("[INFO] Starting initialization phase...")
    load_env_variables()
    db_connection = connect_to_db()
    api_status = test_api_connection()

    if not api_status:
        handle_critical_error(
            "API connection failed. Terminating script.", exit_on_failure=True
        )

    return db_connection


# ---------------------------
# STEP 5: Safe Execution Wrapper
# ---------------------------


def safe_execute_with_logging(function, *args, **kwargs):
    """
    Safely execute a function, logging and handling any exceptions that occur.
    :param function: The function to execute.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.
    :return: The function's result, or None if an exception occurred.
    """
    try:
        return function(*args, **kwargs)
    except Exception as e:
        error_trace = traceback.format_exc()
        log_error(
            f"Unhandled exception in {function.__name__}: {str(e)}\n{error_trace}",
            is_critical=True,
        )
        return None


# CodexKeep Initialization Script - Phase 2: Error Handling and Logging
# Purpose: Log errors, handle failures gracefully, and ensure detailed diagnostics for recovery


# ---------------------------
# STEP 1: Error Logging
# ---------------------------

ERROR_LOG_FILE = "error_log.txt"
ERROR_LOG = []  # In-memory error log for runtime tracking


def log_error(error_message, is_critical=False):
    """
    Log an error to both an in-memory list and a persistent file.
    :param error_message: A description of the error.
    :param is_critical: Whether the error is critical (default: False).
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] {'CRITICAL' if is_critical else 'ERROR'}: {error_message}"
    )

    # Add to in-memory log
    ERROR_LOG.append(log_entry)

    # Append to persistent log file
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry + "\n")

    # Print to console for immediate feedback
    print(log_entry)


# ---------------------------
# STEP 2: Graceful Error Handling
# ---------------------------


def handle_error(error_message, exit_on_failure=False):
    """
    Handle an error by logging it and deciding whether to proceed or exit.
    :param error_message: A description of the error.
    :param exit_on_failure: Whether the script should terminate after this error (default: False).
    """
    log_error(error_message)

    if exit_on_failure:
        print("[INFO] Terminating script due to critical error.")
        sys.exit(1)  # Exit with failure status
    else:
        print("[INFO] Attempting to recover from error...")
        time.sleep(3)  # Optional recovery delay


# ---------------------------
# STEP 3: Exception Wrapper
# ---------------------------


def safe_execute(function, *args, **kwargs):
    """
    Safely execute a function, logging and handling any exceptions that occur.
    :param function: The function to execute.
    :param args: Positional arguments for the function.
    :param kwargs: Keyword arguments for the function.
    :return: The function's result, or None if an exception occurred.
    """
    try:
        return function(*args, **kwargs)
    except Exception as e:
        error_trace = traceback.format_exc()
        log_error(
            f"Unhandled exception in {function.__name__}: {str(e)}\n{error_trace}",
            is_critical=True,
        )
        return None


# ---------------------------
# STEP 4: Batch Error Tracking (for Batches)
# ---------------------------

BATCH_ERRORS = []  # Specific tracking for batch processing


def log_batch_error(batch_num, error_message):
    """
    Log an error specific to a batch during processing.
    :param batch_num: The number of the batch that encountered the error.
    :param error_message: A description of the error.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] BATCH {batch_num}: {error_message}"

    # Add to batch-specific log
    BATCH_ERRORS.append(log_entry)

    # Append to persistent log file
    with open(ERROR_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry + "\n")

    # Print to console for immediate feedback
    print(log_entry)


# CodexKeep Initialization Script - Phase 3: Data Fetching
# Purpose: Fetch the Manifest and related Definitions from the Bungie API


# ---------------------------
# STEP 1: Fetch the Manifest
# ---------------------------


def fetch_manifest():
    """
    Fetch the Manifest from the Bungie API.
    :return: Manifest JSON object or None if the fetch fails.
    """
    print("[INFO] Fetching Manifest...")
    api_key = os.getenv("API_KEY")
    if not api_key:
        handle_critical_error(
            "API key is missing. Please check your .env file.", exit_on_failure=True
        )
        return None

    headers = {"X-API-Key": api_key}
    manifest_url = "https://www.bungie.net/Platform/Destiny2/Manifest/"

    try:
        response = requests.get(manifest_url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("[INFO] Successfully fetched Manifest.")
            return response.json()
        elif response.status_code == 401:
            handle_error(
                "Invalid API key. Please check your .env file.", exit_on_failure=True
            )
            return None
        else:
            log_error(f"Manifest fetch failed: {response.status_code} {response.text}")
            return None
    except Exception as e:
        handle_error(f"Exception occurred while fetching Manifest: {e}")
        return None


# ---------------------------
# STEP 2: Parse Manifest URLs
# ---------------------------


def get_manifest_component_url(manifest_data, component_name):
    """
    Extract the URL for a specific component from the Manifest.
    :param manifest: JSON object containing the Manifest.
    :param component_name: The name of the component to fetch (e.g., DestinyActivityDefinition).
    :return: Full URL to the component definitions or None if parsing fails.
    """
    try:
        paths = manifest_data.get("Response", {}).get(
            "jsonWorldComponentContentPaths", {}
        )
        path = paths.get("en", {}).get(component_name)
        if path:
            full_url = f"https://www.bungie.net{path}"
            print(
                f"[INFO] Successfully extracted URL for {component_name} from Manifest."
            )
            return full_url
        else:
            log_error(f"Component {component_name} is missing in Manifest.")
            return None
    except Exception as e:
        handle_error(f"Error parsing Manifest for {component_name}: {e}")
        return None


# ---------------------------
# STEP 3: Fetch Definitions
# ---------------------------


def fetch_definitions(definition_url, component_name):
    """
    Fetch definitions from the provided URL.
    :param definition_url: URL to fetch the component definitions.
    :param component_name: The name of the component being fetched.
    :return: JSON object containing all definitions or None if the fetch fails.
    """
    if definition_url is None:
        handle_error(
            f"Definition URL for {component_name} is None. Skipping fetch.",
            exit_on_failure=False,
        )
        return None

    print(f"[INFO] Fetching {component_name} definitions...")
    headers = {"X-API-Key": os.getenv("API_KEY")}

    try:
        response = requests.get(definition_url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"[INFO] Successfully fetched {component_name} definitions.")
            return response.json()
        else:
            log_error(
                f"{component_name} definitions fetch failed: {response.status_code} {response.text}"
            )
            return None
    except Exception as e:
        handle_error(
            f"Exception occurred while fetching {component_name} definitions: {e}"
        )
        return None


# ---------------------------
# STEP 4: Process Items Data
# ---------------------------


def process_item_data(items):
    """
    Process raw item data into a structured format suitable for database insertion.
    :param items: JSON object containing item definitions.
    :return: List of dictionaries with cleaned and structured item data.
    """
    print("[INFO] Processing item data...")
    processed_items_list = []

    # Define mappings for categories, subcategories, and damage types
    category_mapping = {
        1: "Weapon",
        20: "Armor",
        40: "Consumable",
        50: "Material",
        60: "Shader",
        70: "Emblem",
        80: "Quest",
        90: "Subclass",
        100: "Mod",
        110: "Ship",
        120: "Sparrow",
        130: "Clan Banner",
        140: "Emote",
        150: "Ghost",
        160: "Finishers",
    }

    subcategory_mapping = {
        2: "Auto Rifle",
        3: "Hand Cannon",
        4: "Pulse Rifle",
        5: "Scout Rifle",
        6: "Fusion Rifle",
        7: "Sniper Rifle",
        8: "Shotgun",
        9: "Machine Gun",
        10: "Rocket Launcher",
        11: "Sidearm",
        12: "Sword",
        13: "Grenade Launcher",
        14: "Linear Fusion Rifle",
        15: "Trace Rifle",
        16: "Bow",
        17: "Glaive",
        21: "Helmet",
        22: "Gauntlets",
        23: "Chest Armor",
        24: "Leg Armor",
        25: "Class Item",
    }

    damage_type_mapping = {
        3373582085: "Kinetic",
        1847026933: "Arc",
        2303181850: "Solar",
        3454344768: "Void",
        151347233: "Stasis",
        3949783978: "Strand",
    }

    for item_id, item_data in items.items():
        try:
            # Extract key fields
            name = item_data["displayProperties"]["name"]
            description = item_data["displayProperties"].get("description", "")
            rarity = item_data["inventory"].get("tierTypeName", "Unknown")
            category_hashes = item_data.get("itemCategoryHashes", [])
            icon = f"https://www.bungie.net{item_data['displayProperties'].get('icon', '')}"
            hash_id = item_data["hash"]

            # Initialize default values for optional fields
            is_exotic = False
            is_quest_item = False
            damage_type = "None"

            # Derive category and subcategory using mappings
            category = "Unknown"
            subcategory = "Unknown"
            if category_hashes:
                category = category_mapping.get(category_hashes[0], "Unknown")
                if len(category_hashes) > 1:
                    subcategory = subcategory_mapping.get(category_hashes[1], "Unknown")

            # Identify if the item is exotic
            if rarity.lower() == "exotic":
                is_exotic = True

            # Identify quest items
            if 16 in category_hashes:  # 16 is the hash for Quest items
                is_quest_item = True

            # Determine damage type for weapons
            if "defaultDamageTypeHash" in item_data:
                damage_type = damage_type_mapping.get(
                    item_data["defaultDamageTypeHash"], "None"
                )

            # Append processed item
            processed_items_list.append(
                {
                    "item_id": item_id,
                    "name": name,
                    "description": description,
                    "rarity": rarity,
                    "category": category,
                    "subcategory": subcategory,
                    "icon": icon,
                    "hash_id": hash_id,
                    "is_exotic": is_exotic,
                    "is_quest_item": is_quest_item,
                    "damage_type": damage_type,
                }
            )
        except KeyError as e:
            log_error(f"Failed to process item {item_id}: Missing key {e}")

    print(f"[INFO] Successfully processed {len(processed_items_list)} items.")
    return processed_items_list


def process_item_drops(activity_definitions, item_definitions):
    """
    Map item drops to activities and enemies based on activity definitions.
    :param activity_definitions: JSON object containing all activity definitions.
    :param item_definitions: JSON object containing all item definitions.
    :return: Tuple of two lists for ActivityDrops and EnemyDrops.
    """
    print("[INFO] Processing item drops...")
    local_activity_drops = []
    local_enemy_drops = []

    for activity_id, activity_data in activity_definitions.items():
        try:
            if "rewards" in activity_data:
                for reward in activity_data["rewards"]:
                    item_hash = reward.get("itemHash")
                    if item_hash in item_definitions:
                        local_activity_drops.append(
                            {
                                "activity_id": activity_id,
                                "item_id": item_hash,
                                "drop_rate": reward.get(
                                    "dropChance", 1.0
                                ),  # Example logic
                            }
                        )
        except KeyError as e:
            log_error(f"Failed to process drops for activity {activity_id}: {e}")

    print(f"[INFO] Processed {len(local_activity_drops)} activity drops.")
    return local_activity_drops, local_enemy_drops


# ---------------------------
# STEP 5: Process Enemies Data
# ---------------------------


def process_enemies_data(activity_definitions):
    """
    Process enemy data based on activity encounters and prepare data for the Enemies table.
    :param activity_definitions: JSON object containing activity definitions.
    :return: List of dictionaries representing processed enemies.
    """
    print("[INFO] Processing Enemies data...")
    processed_enemies = []

    for activity_id, activity_data in activity_definitions.items():
        try:
            # Example: Enemy data derived from activity encounter data
            if "phases" in activity_data:
                for phase in activity_data["phases"]:
                    enemy_name = phase.get("name", "Unknown Enemy")
                    health = phase.get("health", 0)
                    damage_type = phase.get("damageType", "None")
                    zone_id = activity_data.get("locationHash", None)

                    processed_enemies.append(
                        {
                            "enemy_id": f"{activity_id}_{phase['id']}",
                            "name": enemy_name,
                            "type_id": activity_data.get("activityTypeHash"),
                            "zone_id": zone_id,
                            "health": health,
                            "damage_type": damage_type,
                        }
                    )
        except KeyError as e:
            log_error(
                f"Failed to process enemy in activity {activity_id}: Missing key {e}"
            )

    print(f"[INFO] Successfully processed {len(processed_enemies)} enemies.")
    return processed_enemies


# ---------------------------
# STEP 6: Process Locations Data
# ---------------------------


def process_locations_data(location_definitions):
    """
    Process location definitions and prepare data for the Locations table.
    :param location_definitions: JSON object containing all location definitions.
    :return: List of dictionaries representing processed locations.
    """
    print("[INFO] Processing Locations data...")
    processed_locations_list = []

    for location_id, location_data in location_definitions.items():
        try:
            if "displayProperties" not in location_data:
                log_error(f"Missing displayProperties for location {location_id}")
                continue

            name = location_data["displayProperties"]["name"]
            location_type = location_data.get("locationType", "Unknown")
            parent_location = location_data.get("parentLocationHash", None)

            processed_locations_list.append(
                {
                    "location_id": location_id,
                    "name": name,
                    "type": location_type,
                    "parent_location": parent_location,
                }
            )
        except KeyError as e:
            log_error(f"Failed to process location {location_id}: Missing key {e}")

    print(f"[INFO] Successfully processed {len(processed_locations_list)} locations.")
    return processed_locations_list


# ---------------------------
# STEP 7: Process Vendors Data
# ---------------------------


def process_vendors_data(vendor_definitions):
    """
    Process vendor definitions and prepare data for the Vendors table.
    :param vendor_definitions: JSON object containing all vendor definitions.
    :return: List of dictionaries representing processed vendors.
    """
    print("[INFO] Processing Vendors data...")
    processed_vendors_list = []

    for vendor_id, vendor_data in vendor_definitions.items():
        try:
            name = vendor_data["displayProperties"]["name"]
            vendor_type = (
                "Faction"
                if "faction" in vendor_data.get("vendorCategoryIdentifier", "").lower()
                else "NPC"
            )
            location_id = vendor_data.get("vendorLocationHash", None)

            processed_vendors_list.append(
                {
                    "vendor_id": vendor_id,
                    "name": name,
                    "type": vendor_type,
                    "location_id": location_id,
                }
            )
        except KeyError as e:
            log_error(f"Failed to process vendor {vendor_id}: Missing key {e}")

    print(f"[INFO] Successfully processed {len(processed_vendors_list)} vendors.")
    return processed_vendors_list


# ---------------------------
# STEP 8: Process Quests Data
# ---------------------------


def process_quests_data(quest_definitions):
    """
    Process quest definitions and prepare data for the Quests table.
    :param quest_definitions: JSON object containing all quest definitions.
    :return: List of dictionaries representing processed quests.
    """
    print("[INFO] Processing Quests data...")
    processed_quests_list = []

    for quest_id, quest_data in quest_definitions.items():
        try:
            name = quest_data["displayProperties"]["name"]
            description = quest_data["displayProperties"].get("description", "")
            type_name = quest_data.get("questType", "Unknown")
            reward_id = quest_data.get("rewardItemHash", None)

            processed_quests_list.append(
                {
                    "quest_id": quest_id,
                    "name": name,
                    "description": description,
                    "type": type_name,
                    "reward_id": reward_id,
                }
            )
        except KeyError as e:
            log_error(f"Failed to process quest {quest_id}: Missing key {e}")

    print(f"[INFO] Successfully processed {len(processed_quests_list)} quests.")
    return processed_quests_list


# ---------------------------
# STEP 9: Process Currencies Data
# ---------------------------


def process_currencies_data(item_definitions):
    """
    Process item definitions to extract currencies and prepare data for the Currencies table.
    :param item_definitions: JSON object containing all item definitions.
    :return: List of dictionaries representing processed currencies.
    """
    print("[INFO] Processing Currencies data...")
    processed_currencies = []

    for item_id, item_data in item_definitions.items():
        try:
            category_hashes = item_data.get("itemCategoryHashes", [])
            if 100 in category_hashes:  # Example: Currency category hash
                name = item_data["displayProperties"]["name"]
                description = item_data["displayProperties"].get("description", "")
                source = "General"

                processed_currencies.append(
                    {
                        "currency_id": item_id,
                        "name": name,
                        "description": description,
                        "source": source,
                    }
                )
        except KeyError as e:
            log_error(f"Failed to process currency {item_id}: Missing key {e}")

    print(f"[INFO] Successfully processed {len(processed_currencies)} currencies.")
    return processed_currencies


# CodexKeep Initialization Script - Phase 4: Batch Processing
# Purpose: Insert processed data into the database in batches, ensuring reliability and progress tracking

# ---------------------------
# STEP 1: Batch Processing Parameters
# ---------------------------

BATCH_SIZE = 2500  # Number of items per batch
current_batch = []  # Temporary storage for current batch of items
total_inserted = 0  # Track the total number of successful insertions
batch_number = 0  # Track the current batch number

# ---------------------------
# STEP 2: Insert Batch into Database
# ---------------------------


def insert_batch_to_db(conn, batch, current_batch_number):
    """
    Insert a batch of items into the database and clear the temporary batch storage.
    :param conn: Active database connection.
    :param batch: List of item dictionaries to be inserted.
    :param batch_number: Current batch number for logging purposes.
    """
    global total_inserted

    if conn is None:
        log_batch_error(current_batch_number, "Database connection is None.")
        return

    try:
        cur = conn.cursor()
        for item in batch:
            cur.execute(
                """
                INSERT INTO Items (ItemID, Name, Description, Rarity, ImageURL)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (ItemID) DO NOTHING
            """,
                (
                    item["item_id"],
                    item["name"],
                    item["description"],
                    item["rarity"],
                    item["icon"],
                ),
            )

        conn.commit()
        batch_size = len(batch)
        total_inserted += batch_size
        print(
            f"[INFO] Batch {current_batch_number}: Successfully inserted {batch_size} items."
        )
    except psycopg2.Error as e:
        log_batch_error(current_batch_number, f"Database error: {e}")
        conn.rollback()  # Rollback the transaction on failure
    except Exception as e:
        log_batch_error(
            current_batch_number, f"Unexpected error during batch insertion: {e}"
        )
    finally:
        current_batch.clear()  # Clear the batch after processing


# ---------------------------
# STEP 3: Batch Processing Logic
# ---------------------------


def process_items_in_batches(conn, items):
    """
    Process and insert items into the database in batches.
    :param conn: Active database connection.
    :param items: List of processed item dictionaries to be inserted.
    """
    global batch_number
    count = 0

    for item in items:
        current_batch.append(item)
        count += 1

        # If the current batch reaches the defined size, insert it
        if len(current_batch) >= BATCH_SIZE:
            batch_number += 1
            insert_batch_to_db(conn, current_batch, batch_number)

    # Insert any remaining items in the last batch
    if current_batch:
        batch_number += 1
        insert_batch_to_db(conn, current_batch, batch_number)

    print(f"[INFO] Total items processed and inserted: {total_inserted}")


# CodexKeep Initialization Script - Phase 5: Validation
# Purpose: Validate the integrity and format of database records after insertion

# ---------------------------
# STEP 1: Validation Rules
# ---------------------------


def validate_item_row(row):
    """
    Validate a single row from the Items table to ensure data integrity.
    :param row: Tuple containing item data from the database.
    :return: True if the row is valid, False otherwise.
    """
    # Example: Validate that essential fields are not empty or null
    item_id, name, description, rarity, icon = row

    if not item_id or not name or not rarity:
        return False  # Essential fields must not be empty or null
    if len(name) > 255:
        return False  # Name should not exceed the VARCHAR limit
    if description and len(description) > 1000:
        return False  # Description should not exceed the VARCHAR limit
    if icon and not icon.startswith("https://"):
        return False  # Icon URL must be a valid HTTPS URL

    return True


# ---------------------------
# STEP 2: Validate All Records
# ---------------------------


def validate_all_items(conn):
    """
    Validate all rows in the Items table to ensure they meet the defined criteria.
    :param conn: Active database connection.
    """
    if conn is None:
        handle_critical_error(
            "Database connection is None. Cannot validate items.", exit_on_failure=True
        )
        return

    print("[INFO] Starting validation of database records...")

    try:
        cur = conn.cursor()
        cur.execute("SELECT ItemID, Name, Description, Rarity, ImageURL FROM Items")
        rows = cur.fetchall()

        invalid_rows = []
        for row in rows:
            if not validate_item_row(row):
                invalid_rows.append(row)

        # Log validation results
        if invalid_rows:
            print(
                f"[WARNING] {len(invalid_rows)} invalid rows found during validation."
            )
            with open("validation_errors.txt", "w", encoding="utf-8") as file:
                for row in invalid_rows:
                    file.write(f"Invalid row: {row}\n")
            print("[INFO] Validation errors written to 'validation_errors.txt'.")
        else:
            print("[INFO] All records validated successfully. No issues found.")

    except Exception as e:
        handle_error(f"Error during validation: {e}")
    finally:
        cur.close()


# ---------------------------
# STEP 3: Debugging Invalid Rows
# ---------------------------


def debug_invalid_rows():
    """
    Debug function to inspect invalid rows for manual correction.
    This is optional but can be useful for troubleshooting.
    """
    try:
        with open("validation_errors.txt", "r", encoding="utf-8") as file:
            errors = file.readlines()
            for error in errors[:10]:  # Print first 10 invalid rows for inspection
                print(f"[DEBUG] {error.strip()}")
    except FileNotFoundError:
        print("[INFO] No validation errors found. Skipping debug inspection.")


# ---------------------------
# MAIN EXECUTION
# ---------------------------

# ---------------------------
# MAIN EXECUTION FOR PHASE 1
# ---------------------------

if __name__ == "__main__":
    # Initialize connections and prepare for next phases
    connection = initialize_connections()
    if not test_api_connection():
        sys.exit(1)

# ---------------------------
# MAIN EXECUTION FOR PHASE 2
# ---------------------------

if __name__ == "__main__":
    # Example usage of error handling mechanisms
    print("[INFO] Testing error handling mechanisms...")

    # Log a generic error
    log_error("Test error: Something went wrong during initialization.")

    # Simulate handling a critical error
    handle_error("Test critical error: Failed to load API key.", exit_on_failure=False)

    # Simulate a batch error
    log_batch_error(5, "Test batch error: Failed to process batch 5.")

    # Safely execute a sample function
    def sample_function(a, b):
        return a / b  # This will cause a division by zero error if b == 0

    safe_execute_with_logging(sample_function, 10, 0)

    print("[INFO] Error handling tests completed.")

# ---------------------------
# MAIN EXECUTION FOR PHASE 3
# ---------------------------

if __name__ == "__main__":
    print("[INFO] Starting full data fetching and processing...")

    # Initialize connections
    db_conn = initialize_connections()

    # Fetch the Manifest
    manifest = fetch_manifest()
    if manifest is None:
        handle_critical_error(
            "Manifest fetch failed. Terminating script.", exit_on_failure=True
        )

    # Fetch and process data for each component
    component_urls = {
        "items": get_manifest_component_url(manifest, "DestinyInventoryItemDefinition"),
        "activities": get_manifest_component_url(manifest, "DestinyActivityDefinition"),
        "locations": get_manifest_component_url(manifest, "DestinyLocationDefinition"),
        "vendors": get_manifest_component_url(manifest, "DestinyVendorDefinition"),
        "quests": get_manifest_component_url(manifest, "DestinyQuestDefinition"),
    }

    # Ensure component URLs are valid
    if not all(component_urls.values()):
        handle_critical_error(
            "One or more component URLs are invalid. Terminating script.",
            exit_on_failure=True,
        )

    # Fetch data for each table
    items_table = fetch_definitions(component_urls["items"], "Items")
    activities_table = fetch_definitions(component_urls["activities"], "Activities")
    locations_table = fetch_definitions(component_urls["locations"], "Locations")
    vendors_table = fetch_definitions(component_urls["vendors"], "Vendors")
    quests_table = fetch_definitions(component_urls["quests"], "Quests")

    # Process each table
    processed_items = process_item_data(items_table)
    processed_activities = process_enemies_data(activities_table)
    processed_locations = process_locations_data(locations_table)
    processed_vendors = process_vendors_data(vendors_table)
    processed_quests = process_quests_data(quests_table)

    # Fetch data for ItemDrops
    activity_drops, enemy_drops = process_item_drops(activities_table, items_table)

    # Debug: Print a sample drop
    if activity_drops:
        print("[DEBUG] Sample activity drop:", activity_drops[0])

    print("[INFO] Full data fetching and processing completed successfully.")

# ---------------------------
# MAIN EXECUTION FOR PHASE 4
# ---------------------------

if __name__ == "__main__":
    print("[INFO] Starting batch processing phase...")

    # Assuming `conn` is the database connection and `processed_items` is the list of item dictionaries
    try:
        connection = connect_to_db()  # Reuse the connection function from Phase 1
        process_items_in_batches(connection, processed_items)
    except Exception as e:
        handle_critical_error(
            f"Critical error during batch processing: {e}", exit_on_failure=True
        )
    finally:
        if connection:
            connection.close()  # Ensure the database connection is properly closed

    print("[INFO] Batch processing phase completed successfully.")

# ---------------------------
# MAIN EXECUTION FOR PHASE 5
# ---------------------------

if __name__ == "__main__":
    print("[INFO] Starting validation phase...")

    # Assuming `conn` is the database connection
    try:
        connection = connect_to_db()  # Reuse the connection function from Phase 1
        validate_all_items(connection)
        debug_invalid_rows()
    except Exception as e:
        handle_critical_error(
            f"Critical error during validation: {e}", exit_on_failure=True
        )
    finally:
        if connection:
            connection.close()  # Ensure the database connection is properly closed

    print("[INFO] Validation phase completed successfully.")
