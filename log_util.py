# log_util.py
# Eigener Logger. Das logging-Modul war uns 2013 "zu viel Magie".
# (A homemade logger. The logging module felt like "too much magic" in 2013.)

import time

LOG_LINES: list[str] = []
DEBUG = False


def log(message: str) -> None:
    """Add a timestamped message to the log."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"

    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a debug message when debugging is enabled."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Write buffered log messages to a file."""
    with open(path, "a", encoding="utf-8") as file:
        for line in LOG_LINES:
            file.write(f"{line}\n")

    LOG_LINES.clear()
