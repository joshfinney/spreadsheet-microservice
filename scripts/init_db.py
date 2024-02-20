import os
import sqlite3
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

# Path to your SQLite database
database_path = "../cells.db"

# SQL command to create your table(s)
create_table_sql = """
CREATE TABLE IF NOT EXISTS cell (
    id TEXT PRIMARY KEY,
    formula TEXT NOT NULL
);
"""

def reset_database():
    # Remove the existing database file if it exists
    if os.path.exists(database_path):
        os.remove(database_path)
        logging.info(f"Removed existing database at {database_path}")
    
    # Create a new database and initialize it with the schema
    try:
        with sqlite3.connect(database_path) as conn:
            # Create table(s)
            conn.execute(create_table_sql)
            logging.info("Database schema initialized.")
    except Exception as e:
        logging.error(f"Failed to initialize database schema: {e}")

if __name__ == "__main__":
    reset_database()