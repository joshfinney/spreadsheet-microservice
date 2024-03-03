import logging

from app.services.firebase_service import firebase_delete_cell, firebase_get_cell, firebase_list_cells, firebase_put_cell
from .db_service import DBService
from app.utilities.parser import evaluate_expression, ParserError
from app.utilities.logging_config import setup_logging
from flask import current_app

setup_logging()

class CellService:
    @staticmethod
    def create_or_update_cell(cell_id, formula):
        setup_logging()

        if not cell_id or not formula:  # Ensure both cell_id and formula are provided
            raise ValueError("Both Cell ID and formula must be provided")
        
        if not formula:  # Validate non-empty formula
            raise ValueError("Formula cannot be empty")
        
        if current_app.config.get('FIREBASE_URL', False):
            cell_data = {"formula": formula}
            response_status = firebase_put_cell(cell_id, cell_data)            
            if response_status == 204:
                return False
            elif response_status == 201:
                return True
        else:
            # Correctly handle the return value from DBService.upsert_cell
            was_created = DBService.upsert_cell(cell_id, formula)
            # There's no separate 'success' flag; operations that fail will throw exceptions
            
            return was_created  # True for create, False for update

    @staticmethod
    def get_cell_value(cell_id):
        setup_logging()

        logging.debug(f"Attempting to retrieve value for cell {cell_id}.")  # Log cell ID being processed

        if current_app.config.get('FIREBASE_URL', False):
            # Handle Firebase storage
            cell = firebase_get_cell(cell_id)
            if cell is None:
                return 0  # Assuming a missing cell returns 0
            formula = cell.get('formula', '0')
        else:
            # Handle SQLite storage
            cell = DBService.get_cell_by_id(cell_id)
            if cell is None:
                logging.error(f"Cell {cell_id} not found")
                return 0  # Assuming a missing cell returns 0
        
        # Log the formula after confirming the cell exists
        formula = cell['formula']
        logging.info(f"Fetching value for cell {cell_id} with formula: {formula}")

        try:
            return float(formula)
        except ValueError:
            pass

        try:
            # If cell['formula'] is a reference to another cell or a computation, evaluate it
            value = evaluate_expression(formula, lambda x: CellService.get_cell_value(x))
            logging.info(f"Resolved cell {cell_id} to value {value}")
            return value if isinstance(value, (int, float)) else 0
        except ParserError as e:
            logging.error(f"Error evaluating cell {cell_id}: {e}")
            raise ValueError(f"Error evaluating cell {cell_id}: {e}")


    @staticmethod
    def delete_cell(cell_id):
        setup_logging()

        if current_app.config.get('FIREBASE_URL', False):
            # Handle Firebase storage
            firebase_delete_cell(cell_id)
        else:
            # Handle SQLite storage
            DBService.delete_cell(cell_id)

    @staticmethod
    def list_cells():
        setup_logging()

        if current_app.config.get('FIREBASE_URL', False):
            # Handle Firebase storage
            return firebase_list_cells()
        else:
            # Handle SQLite storage
            return DBService.list_all_cells()