import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Generate log filename with timestamp
timestamp = datetime.now().strftime('%Y%m%d')
log_file = f"logs/pipeline_{timestamp}.log"

# Configure logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def get_logger(name):
    """
    Get a logger with the specified name.

    Args:
        name (str): Name for the logger (typically module or component name).

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
