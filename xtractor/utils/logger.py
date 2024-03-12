import os
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define the log format
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a stream handler for console output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)

log_path = os.path.join(os.getcwd(), "xtractor", "logs", "logs.log")

# Create a file handler for log file output
file_handler = logging.FileHandler(log_path, "a", "utf-8")
file_handler.setFormatter(log_format)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
