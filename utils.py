import re
from config import REG_PATTERN


__all__ = ["is_python_file"]


def is_python_file(file_name):
    if re.match(REG_PATTERN["python_file"], file_name):
        return True

    return False
