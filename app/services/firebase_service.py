import os
import requests
import json

# Firebase configuration
FIREBASE = os.environ.get('FBASE')
FIREBASE_URL = FIREBASE + "cell//cel"

def firebase_get_cell(cell_id):
    """Retrieve a cell from Firebase"""
    response = requests.get(f'{FIREBASE_URL}/cells/{cell_id}.json?auth={FIREBASE_TOKEN}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def firebase_put_cell(cell_id, cell_data):
    """Create or update a cell in Firebase"""
    response = requests.put(f'{FIREBASE_URL}/cells/{cell_id}.json?auth={FIREBASE_TOKEN}', json=cell_data)
    return response.status_code

def firebase_delete_cell(cell_id):
    """Delete a cell from Firebase"""
    response = requests.delete(f'{FIREBASE_URL}/cells/{cell_id}.json?auth={FIREBASE_TOKEN}')
    return response.status_code

def firebase_list_cells():
    """List all cells from Firebase"""
    response = requests.get(f'{FIREBASE_URL}/cells.json?auth={FIREBASE_TOKEN}')
    if response.status_code == 200:
        return list(response.json().keys())
    else:
        return []
