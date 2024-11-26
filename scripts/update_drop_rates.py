# Script to update drop rates
import psycopg2

# Connect to database
conn = psycopg2.connect("dbname=codexkeep user=your_username password=your_password")
cur = conn.cursor()

# Example: Update drop rates
cur.execute(
    """
UPDATE EnemyDrops
SET DropRate = 0.05
WHERE EnemyID = 1 AND ItemID = 1
"""
)

conn.commit()
cur.close()
conn.close()

print("Update drop rates script")
