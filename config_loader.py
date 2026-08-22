# config_loader.py
# Liest settings.cfg. Selbst geschrieben, weil uns ConfigParser 2013 "zu kompliziert" war.
# (Reads settings.cfg. Hand-rolled, because ConfigParser felt "too complicated" in 2013.)

from pathlib import Path

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | Path | None = None) -> dict[str, str]:
    """Load known settings from the configuration file."""
    config_path = Path(path or SETTINGS_FILE)
    settings: dict[str, str] = {}

    with config_path.open(encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = (part.strip() for part in line.split("=", 1))

            if key in KNOWN_KEYS:
                settings[key] = value

    return settings


def get_int(
    settings: dict[str, str],
    key: str,
    fallback: int,
) -> int:
    """Return a setting as an integer or use the fallback."""
    try:
        return int(settings[key])
    except (KeyError, ValueError):
        return fallback


def get_setting(
    settings: dict[str, str],
    key: str,
    fallback: str = "",
) -> str:
    """Return a setting or its fallback."""
    return settings.get(key, fallback)
