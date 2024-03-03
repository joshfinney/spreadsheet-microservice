import os
import sqlite3
import logging
from flask import current_app
import requests  # Import requests library

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

# Firebase configuration
firebase_url = f"https://{os.environ.get('FBASE')}.europe-west1.firebasedatabase.app"

# Path to your SQLite database
database_path = "../cells.db"

# SQL command to create your table(s)
create_table_sql = """
CREATE TABLE IF NOT EXISTS cell (
    id TEXT PRIMARY KEY,
    formula TEXT NOT NULL
);
"""

def reset_firebase_database():
    """Delete all cells from Firebase database"""
    try:
        response = requests.delete(f"{firebase_url}/cells.json")  # Assumes cells are stored under 'cells' node
        if response.status_code in [200, 204]:
            logging.info("All cells deleted from Firebase database.")
        else:
            logging.error(f"Failed to delete cells from Firebase database: {response.status_code}")
    except Exception as e:
        logging.error(f"Exception occurred while deleting cells from Firebase database: {e}")

def reset_sqlite_database():
    """Reset SQLite database by removing existing file and recreating schema"""
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

def reset_database():
    if os.environ.get('FBASE'):
        reset_firebase_database()
    else:
        reset_sqlite_database()

if __name__ == "__main__":
    reset_database()
