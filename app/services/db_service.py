import sqlite3
from flask import current_app, g
import logging
from app.utilities.logging_config import setup_logging

setup_logging()

def get_db():
    if 'db' not in g:
        setup_logging()

        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    setup_logging()

    db = g.pop('db', None)
    if db is not None:
        db.close()

class DBService:

    @staticmethod
    def upsert_cell(cell_id, formula):
        setup_logging()

        logging.info(f"Upserting cell {cell_id} with formula {formula}")
        db = get_db()
        # Check if the cell exists first
        cell_exists = db.execute(
            'SELECT 1 FROM cell WHERE id = ?',
            (cell_id,)
        ).fetchone() is not None

        if cell_exists:
            db.execute('UPDATE cell SET formula = ? WHERE id = ?', (formula, cell_id))
        else:
            db.execute('INSERT INTO cell (id, formula) VALUES (?, ?)', (cell_id, formula))
        db.commit()
        
        return not cell_exists  # Returns True if it was a create operation, False if update

    @staticmethod
    def get_cell_by_id(cell_id):
        setup_logging()

        logging.info(f"Fetching cell by ID: {cell_id}")
        db = get_db()
        cell = db.execute(
            'SELECT id, formula FROM cell WHERE id = ?',
            (cell_id,)
        ).fetchone()
        if cell is not None:
            logging.info(f"Cell {cell_id} found with formula: {cell['formula']}")
        else:
            logging.info(f"Cell {cell_id} not found.")
        return cell

    @staticmethod
    def delete_cell(cell_id):
        setup_logging()

        db = get_db()
        db.execute('DELETE FROM cell WHERE id = ?', (cell_id,))
        db.commit()

    @staticmethod
    def list_all_cells():
        setup_logging()

        db = get_db()
        cells = db.execute('SELECT id FROM cell').fetchall()
        return [cell['id'] for cell in cells]