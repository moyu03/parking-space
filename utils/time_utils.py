# utils/time_utils.py

import time
from datetime import datetime

def timestamp_to_str(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
