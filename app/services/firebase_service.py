import logging
import os
import requests
import json
from flask import current_app
from app.utilities.logging_config import setup_logging

setup_logging()

def firebase_get_cell(cell_id):
    """Retrieve a cell from Firebase"""
    firebase_url = current_app.config['FIREBASE_URL']

    response = requests.get(f'{firebase_url}/cells/{cell_id}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def firebase_put_cell(cell_id, cell_data):
    """Create or update a cell in Firebase"""
    firebase_url = current_app.config['FIREBASE_URL']
    try:
        # Check if the cell already exists
        existing_cell_response = requests.get(f'{firebase_url}/cells/{cell_id}.json')
        existing_cell_response.raise_for_status()  # Raise an error for bad responses

        if existing_cell_response.status_code == 200 and existing_cell_response.json() is not None:
            # Update existing cell
            response = requests.put(f'{firebase_url}/cells/{cell_id}.json', json=cell_data)
            response.raise_for_status()
            logging.info("WE'RE IN UPDATE")
            return 204  # No Content
        else:
            # Create new cell
            response = requests.put(f'{firebase_url}/cells/{cell_id}.json', json=cell_data)
            response.raise_for_status()
            logging.info("WE'RE IN CREATE")
            return 201  # Created
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error when accessing Firebase: {e}")
        return 500
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from Firebase.")
        return 500

def firebase_delete_cell(cell_id):
    """Delete a cell from Firebase"""
    firebase_url = current_app.config['FIREBASE_URL']

    response = requests.delete(f'{firebase_url}/cells/{cell_id}')
    return response.status_code

def firebase_list_cells():
    """List all cells from Firebase"""
    firebase_url = current_app.config['FIREBASE_URL']
    try:
        response = requests.get(f'{firebase_url}/cells.json')  # Ensure to include .json at the end
        response.raise_for_status()  # This will raise for HTTP errors

        # Check if response is not empty and is a JSON object
        if response.text:  # Checks if response body is not empty
            data = response.json()  # Attempts to parse JSON
            if data and isinstance(data, dict):  # Checks if data is a dictionary (JSON object)
                return list(data.keys())
            else:
                logging.error("Firebase response is not a JSON object.")
                return []
        else:
            logging.info("Firebase response is empty.")
            return []
    except requests.RequestException as e:
        logging.error(f"Request to Firebase failed: {e}")
        return []
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from Firebase response.")
        return []
