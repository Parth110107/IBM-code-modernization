# test_km_wachter.py
from km_wachter import needs_service, wear_percent
def test_wear_percent_keeps_partial_interval():
    assert wear_percent(12000, 15000) == 80
def test_almost_due_car_is_flagged():
    """A nearly worn car must be flagged."""
    assert needs_service(
        {
            "id": "VOS-4471",
            "odometer": 14900,
            "last_service_km": 0,
        }
    ) is True
def test_missing_reading_is_not_treated_as_zero():
    """A missing service reading must not falsely flag a car."""
    assert needs_service(
        {
            "id": "VOS-7788",
            "odometer": 92000,
        }
    ) is False
