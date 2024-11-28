# CodexKeep/scripts/batch_processing.py

import os
from error_handling import log_batch_error

try:
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
    if BATCH_SIZE <= 0:
        raise ValueError("Batch size must be greater than 0.")
except ValueError as e:
    log_batch_error(0, f"Invalid BATCH_SIZE value: {e}. Defaulting to 1000.")
    BATCH_SIZE = 1000


def insert_batch_to_db(conn, batch, batch_number):
    """
    Insert a batch of items into the database.
    """
    if not conn:
        log_batch_error(batch_number, "Database connection is None.")
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
        print(f"[INFO] Batch {batch_number}: Inserted {len(batch)} items.")
    except Exception as e:
        log_batch_error(batch_number, f"Failed to insert batch: {e}")
        conn.rollback()


def process_items_in_batches(conn, items):
    """
    Process items in batches and insert them into the database.
    """
    batch = []
    batch_number = 0
    for item in items:
        batch.append(item)
        if len(batch) >= BATCH_SIZE:
            batch_number += 1
            insert_batch_to_db(conn, batch, batch_number)
            batch.clear()

    if batch:
        batch_number += 1
        insert_batch_to_db(conn, batch, batch_number)

    print(f"[INFO] Finished batch processing. Total batches: {batch_number}")


if __name__ == "__main__":
    print("[INFO] This script is intended to be imported, not run directly.")
