import logging
import sys
from pathlib import Path
from colorama import just_fix_windows_console

LOG_DIR= Path("log")
LOG_DIR.mkdir(exist_ok=True)

just_fix_windows_console()

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[90m",     # gray
        logging.INFO: "\033[36m",      # cyan
        logging.WARNING: "\033[33m",   # yellow
        logging.ERROR: "\033[91m",     # bright red 
        logging.CRITICAL: "\033[1;97;41m",  # bold white text on red background
    }
    RESET = "\033[0m"

    def format(self, record):
        record_color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        # print(f"PRINTEED::{record_color = }\n{self.RESET = }")
        return rf"{record_color}{message}{self.RESET}"

def setup_logging():
    log_format = (
        "%(name)s.%(funcName)s | "
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if setup_logging() is called again
    root_logger.handlers.clear()

    # stream handler
    std_logger = logging.StreamHandler(sys.stdout)
    std_logger.setFormatter(
        ColoredFormatter(log_format)
    )
    root_logger.addHandler(std_logger)

    # file handler
    file_handler = logging.FileHandler(
        LOG_DIR / "application.log",
        encoding = "utf-8"
    )
    file_handler.setFormatter(
        logging.Formatter(log_format)
    )
    root_logger.addHandler(file_handler)
    