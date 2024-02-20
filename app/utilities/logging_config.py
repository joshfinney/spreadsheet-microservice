import logging

class CustomFilter(logging.Filter):
    def filter(self, record):
        if "queue_event" in record.getMessage() or "NativeEvent" in record.getMessage() or "event_type" in record.getMessage():
            return False  # Exclude these logs
        return True

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Apply filter to Flask and Werkzeug loggers specifically
    flask_logger = logging.getLogger('flask.app')
    werkzeug_logger = logging.getLogger('werkzeug')
    custom_filter = CustomFilter()
    flask_logger.addFilter(custom_filter)
    werkzeug_logger.addFilter(custom_filter)

    # Optionally, adjust the logging level for these loggers
    # flask_logger.setLevel(logging.DEBUG)
    # werkzeug_logger.setLevel(logging.DEBUG)

# Then, ensure you call setup_logging() early in your application setup