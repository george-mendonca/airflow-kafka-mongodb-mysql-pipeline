"""
Professional Logging Setup

This module provides a centralized logging configuration for the ETL pipeline.
It sets up both console and file logging with configurable log levels.

Features:
- Console output for immediate feedback
- File output for persistent logging (app.log)
- Configurable log level via LOG_LEVEL environment variable
- Standardized format: timestamp - module - level - message

Usage:
    from src.utils.logger import setup_logger
    
    logger = setup_logger()
    logger.info("Starting ETL process")
    logger.warning("High memory usage detected")
    logger.error("Failed to connect to database")

Configuration:
    Set LOG_LEVEL environment variable to one of:
    - DEBUG: Detailed information for diagnosing problems
    - INFO: General information about application flow (default)
    - WARNING: Something unexpected happened, but application continues
    - ERROR: A serious problem occurred
    - CRITICAL: Application may be unable to continue

Example:
    # In .env file or environment
    LOG_LEVEL=INFO
    
    # In your code
    logger = setup_logger()
    logger.info("Processing batch of 100 records")
    logger.debug("Record details: {...}")  # Only shown if LOG_LEVEL=DEBUG
"""

import logging
import os

# Read log level from environment variable
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


def setup_logger(name=None):
    """
    Configure and return a logger instance with console and file handlers.
    
    Args:
        name (str, optional): Logger name. If None, uses the calling module's name.
        
    Returns:
        logging.Logger: Configured logger instance
        
    Example:
        >>> logger = setup_logger(__name__)
        >>> logger.info("Application started")
        2024-01-20 10:30:00,123 - mymodule - INFO - Application started
    """
    logger = logging.getLogger(name or __name__)
    logger.setLevel(LOG_LEVEL)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create console handler and set level
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)

    # Create file handler and set level
    fh = logging.FileHandler('app.log')
    fh.setLevel(LOG_LEVEL)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Add formatter to handlers
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger