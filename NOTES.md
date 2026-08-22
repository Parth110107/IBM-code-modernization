# What I checked, and what the agent got wrong

## What the agent got wrong

The main bug was in the wear calculation. The code used `//` instead of `/`, which removed the decimal part of the ratio. That meant a car could be between 80% and 99.9% worn but still report 0% wear.

I also caught that the warning threshold had been changed from 80% to 85%. I left the original 80% rule unchanged because the task specifically said not to change what the service decides.

I also found a separate quiet bug in `fleet_utils.py`: the km-to-miles conversion used `1.609` instead of about `0.621371`.

## What I checked before I accepted the work

I checked the code and tests instead of trusting the agent's summary. I added a test for 12,000 km out of a 15,000 km service interval, which must report 80% wear. I also added a test proving that a missing `last_service_km` value does not crash the fleet report.

I checked that the 15,000 km interval and 80% warning threshold stayed unchanged in both the Python code and `settings.cfg`.

## What the data actually said

The fleet history showed that total mileage and age were almost the same for cars that broke down and cars that kept going. The clearer differences were kilometres since service, average daily kilometres, and load factor.

I used those three factors for the simple risk score instead of assuming that older or higher-mileage cars were automatically the riskiest.
