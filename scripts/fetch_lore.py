# Script to fetch lore data
import psycopg2

# Connect to database
conn = psycopg2.connect("dbname=codexkeep user=your_username password=your_password")
cur = conn.cursor()

# Insert lore entry
cur.execute(
    """
INSERT INTO LoreEntries (BookID, Title, Content)
VALUES (1, 'The Last Word', 'Excerpt about The Last Word.');
"""
)

conn.commit()
cur.close()
conn.close()

print("Fetch lore script")
