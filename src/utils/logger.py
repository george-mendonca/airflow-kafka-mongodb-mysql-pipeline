import logging
import os

# Read log level from settings (assuming it's an environment variable)
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)

    # Create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)

    # Create file handler and set level
    fh = logging.FileHandler('app.log')
    fh.setLevel(LOG_LEVEL)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to handlers
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger