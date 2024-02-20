from app import create_app
import logging
from app.utilities.logging_config import setup_logging

setup_logging()

app = create_app()

if __name__ == '__main__':

    app.run(debug=True, port=3000)