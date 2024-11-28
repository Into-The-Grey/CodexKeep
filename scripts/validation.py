# CodexKeep/scripts/validation.py

from error_handling import log_error, handle_critical_error


def validate_item_row(row):
    """
    Validate a single row from the Items table.
    """
    try:
        item_id, name, description, rarity, icon = row
    except ValueError as e:
        log_error(f"Row unpacking error: {e}")
        return False

    if not item_id or not isinstance(item_id, (str, int)):
        log_error(f"Invalid item_id: {item_id}")
        return False
    if not name or len(name.strip()) == 0 or len(name) > 255:
        log_error(f"Invalid name: {name}")
        return False
    if description and len(description) > 1000:
        log_error(f"Description too long: {description}")
        return False
    if icon and not icon.startswith("https://"):
        log_error(f"Invalid icon URL: {icon}")
        return False

    valid_rarity = {"Common", "Uncommon", "Rare", "Legendary", "Exotic"}
    if rarity not in valid_rarity:
        log_error(f"Invalid rarity: {rarity}")
        return False
    return True


def validate_all_items(conn):
    """
    Validate all rows in the Items table.
    """
    if not conn:
        handle_critical_error("Database connection is None.", exit_on_failure=True)

    cur = conn.cursor()
    try:
        cur.execute("SELECT ItemID, Name, Description, Rarity, ImageURL FROM Items")
        rows = cur.fetchall()
        invalid_rows = [row for row in rows if not validate_item_row(row)]
        if invalid_rows:
            print(f"[WARNING] Found {len(invalid_rows)} invalid rows.")
            with open("validation_errors.txt", "w", encoding="utf-8") as f:
                for row in invalid_rows:
                    f.write(f"Invalid row: {row}\n")
        else:
            print("[INFO] All rows validated successfully.")
    except Exception as e:
        log_error(f"Validation failed: {e}")
    finally:
        cur.close()


if __name__ == "__main__":
    print("[INFO] This script is intended to be imported, not run directly.")
