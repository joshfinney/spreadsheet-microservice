import json
from flask import Blueprint, request, jsonify, make_response
from .services.cell_service import CellService
import logging
from .utilities.logging_config import setup_logging

setup_logging()

bp = Blueprint('cells', __name__, url_prefix='/cells')

@bp.route('/<cell_id>', methods=['PUT'])
def create_or_update_cell(cell_id):
    setup_logging()

    data = request.get_json()

    # Check data
    if not data:
        logging.warning(f"Attempt to create or update cell without request body.")
        return make_response("", 400)
    
    if 'id' not in data:
        logging.warning(f"Attempt to create or update cell without ID.")
        return make_response("", 400)
    
    if data['id'] != cell_id:
        logging.warning(f"There is a mismatch in request body ID and url ID.")
        return make_response("", 400)

    if 'formula' not in data:
        logging.warning(f"Attempt to create or update cell without formula. Cell ID: {cell_id}")
        return make_response("", 400)

    formula = data['formula']

    if not isinstance(formula, str):
        logging.warning(f"Formula must be a string. Received type: {type(formula)}. Cell ID: {cell_id}")
        return make_response("", 400)
    
    try:
        was_created = CellService.create_or_update_cell(cell_id, formula)
        if was_created:
            logging.info(f"Cell {cell_id} created successfully.")
            return make_response("", 201)
        else:
            logging.info(f"Cell {cell_id} updated successfully.")
            return make_response("", 204)  # Corrected to return 204 on update
    except ValueError as e:
        logging.error(f"Error during cell creation/updating: {e}")
        return make_response("", 400)
    except Exception as e:
        logging.error(f"Internal server error: {e}")
        return make_response("", 500)


@bp.route('/<cell_id>', methods=['GET'])
def get_cell(cell_id):
    setup_logging()

    logging.info(f"Received GET request for cell {cell_id}")
    try:
        cell_value = CellService.get_cell_value(cell_id)
        
        if cell_value is None:
            logging.info(f"Cell not found. Cell ID: {cell_id}")
            return make_response("", 404)
        
        logging.info(f"Completed GET request for cell {cell_id}, value {cell_value}")
        
        response_data = {"formula": str(cell_value), "id": cell_id}
        
        # Portable:
        # response = jsonify(response_data)
        # return response

        # Blue specific:
        # Convert dictionary to string and ensure no spaces are included between keys and values
        response_str = json.dumps(response_data, separators=(',', ':'))
        
        # Create a response with the correct content-type
        response = make_response(response_str)
        response.headers['Content-Type'] = 'application/json'
        
        return response
    
    except Exception as e:
        logging.error(f"Internal server error: {e}")
        return make_response("", 500)

@bp.route('/<cell_id>', methods=['DELETE'])
def delete_cell(cell_id):
    setup_logging()

    try:
        CellService.delete_cell(cell_id)
        logging.info(f"Cell {cell_id} deleted successfully.")
        return make_response("", 204)
    except Exception as e:
        logging.error(f"Internal server error: {e}")
        return make_response("", 500)

@bp.route('/', methods=['GET'])
@bp.route('', methods=['GET'])  # Handles without trailing slash
def list_cells():
    setup_logging()

    try:
        cells = CellService.list_cells()
        logging.info("Cells listed successfully.")
        logging.info(cells)
        return jsonify(cells)
    except Exception as e:
        logging.error(f"Internal server error: {e}")
        return make_response("", 500)