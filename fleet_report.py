# fleet_report.py
# Prints the nightly fleet-health summary for Vossberg Mobility.
# Written in 2014. Runs every morning. Never cleaned up.

from config_loader import get_setting, load_settings
from km_wachter import SERVICE_INTERVAL_KM, needs_service, wear_percent
from log_util import flush_log, log

import fleet_utils


def car_wear(car: dict) -> float:
    """Return the wear percentage for one car."""
    last = car.get("last_service_km")

    if last is None:
        return 0.0

    return wear_percent(
        car["odometer"] - last,
        SERVICE_INTERVAL_KM,
    )


def fleet_summary(fleet: list[dict]) -> dict:
    """Return basic fleet wear and service statistics."""
    total = 0.0
    due = 0

    for car in fleet:
        total += car_wear(car)

        if needs_service(car):
            due += 1

    average = total / len(fleet) if fleet else 0.0

    return {
        "count": len(fleet),
        "due": due,
        "average_wear": average,
    }


def print_report(fleet: list[dict]) -> None:
    """Print and log the nightly fleet report."""
    settings = load_settings()

    log(get_setting(settings, "report_title", "Nightly fleet report"))

    summary = fleet_summary(fleet)

    print(f"Fleet: {summary['count']} cars")
    print(f"Due for service: {summary['due']}")
    print(f"Average wear: {summary['average_wear']:.1f}%")

    total_km = sum(car["odometer"] for car in fleet)

    print(
        "Fleet distance: "
        f"{fleet_utils.format_number(fleet_utils.km_to_miles(total_km))} miles"
    )

    flush_log(get_setting(settings, "log_file", "km_wachter.log"))
