import logging
import sys


def setup_logger(name: str, level: str = "DEBUG"):
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, level.upper(), logging.DEBUG),
        format=f"%(asctime)s - %(levelname)s - {name} - %(message)s",
    )
