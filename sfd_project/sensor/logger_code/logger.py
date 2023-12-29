import logging
import os
from datetime import datetime

from from_root import from_root

# log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOGFILE_ROOT_PATH = "sfd_project/logs"
# path to log file
# Note: do not add LOG_FILE while creating logs_path
logs_path = os.path.join(from_root(), LOGFILE_ROOT_PATH)

# create logs directory if it does not exist
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
# basic logging configuration to log to a file with INFO level.
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
