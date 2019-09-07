"""Utility functions."""

import logging
import os
import sys

def read_file(path):
    """Read file contents and return it as a string."""
    if path and os.path.exists(path):
        with open(path, "r") as file_handle:
            data = file_handle.read()
    else:
        data = ""
    return data


def setup_logger():
    """Set a logger up with script name logging to STDERR."""
    logger = logging.getLogger(os.path.basename(sys.argv[0]))
    logger.addHandler(logging.StreamHandler(stream=sys.stderr))
    logger.setLevel(logging.DEBUG)
    return logger
