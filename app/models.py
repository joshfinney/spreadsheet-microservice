import sqlite3
from flask import g, current_app

from app.utilities.logging_config import setup_logging

def get_db():
    setup_logging()
    
    if 'db' not in g:
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

def init_db(app):
    setup_logging()
    
    with app.app_context():
        db = get_db()
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
    app.teardown_appcontext(close_db)