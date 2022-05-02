from datetime import datetime
import time


def get_unique_timestamp():
    time.sleep(1)
    return datetime.strftime(datetime.utcnow(), "%s")
