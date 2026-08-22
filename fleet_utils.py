# fleet_utils.py
# Sammelbecken fuer Helfer seit 2013. Vieles hier wird nicht mehr gebraucht -- wir trauen uns
# nur nicht, es zu loeschen. (Catch-all helpers since 2013. Much of this is unused -- we just
# never dared to delete anything.)

MILES_PER_KM = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number with one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a percentage."""
    return f"{value:.0f}%"


def mean(values: list[float]) -> float:
    """Return the mean of a list of values."""
    if not values:
        return 0.0

    return sum(values) / len(values)


def is_due(pct: float, threshold: float) -> bool:
    """Return True when wear reaches the threshold."""
    return pct >= threshold


def parse_service_date(text: str) -> tuple[int, int, int] | None:
    """Parse a DD.MM.YYYY service date."""
    parts = text.split(".")

    if len(parts) != 3:
        return None

    try:
        day, month, year = (int(part) for part in parts)
    except ValueError:
        return None

    return year, month, day


def chunk_list(items: list, size: int) -> list[list]:
    """Split a list into chunks of the requested size."""
    if size <= 0:
        raise ValueError("size must be greater than zero")

    return [
        items[index:index + size]
        for index in range(0, len(items), size)
    ]
