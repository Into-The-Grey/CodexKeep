# CodexKeep/scripts/data_processing.py

from error_handling import log_error


def process_item_data(items):
    """
    Process raw item data into a structured format suitable for database insertion.
    """
    print("[INFO] Processing item data...")
    processed_items_list = []

    for item_id, item_data in items.items():
        try:
            name = item_data["displayProperties"]["name"]
            description = item_data["displayProperties"].get("description", "")
            rarity = item_data["inventory"].get("tierTypeName", "Unknown")
            category_hashes = item_data.get("itemCategoryHashes", [])
            icon = f"https://www.bungie.net{item_data['displayProperties'].get('icon', '')}"
            processed_items_list.append(
                {
                    "item_id": item_id,
                    "name": name,
                    "description": description,
                    "rarity": rarity,
                    "category_hashes": category_hashes,
                    "icon": icon,
                }
            )
        except KeyError as e:
            log_error(f"Failed to process item {item_id}: Missing key {e}")
    print(f"[INFO] Successfully processed {len(processed_items_list)} items.")
    return processed_items_list


def process_activity_drops(activities, items):
    """
    Process activity drops based on activity definitions.
    """
    print("[INFO] Processing activity drops...")
    activity_drops = []
    for activity_id, activity_data in activities.items():
        try:
            for reward in activity_data.get("rewards", []):
                item_id = reward.get("itemHash")
                if item_id in items:
                    activity_drops.append(
                        {
                            "activity_id": activity_id,
                            "item_id": item_id,
                            "drop_rate": reward.get("dropChance", 1.0),
                        }
                    )
        except KeyError as e:
            log_error(f"Failed to process drops for activity {activity_id}: {e}")
    print(f"[INFO] Processed {len(activity_drops)} activity drops.")
    return activity_drops


if __name__ == "__main__":
    print("[INFO] This script is intended to be imported, not run directly.")
