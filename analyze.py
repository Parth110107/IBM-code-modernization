# analyze.py
"""Analyze fleet history and rank cars by breakdown risk.

The strongest separation in the supplied history is:
1. km_since_service
2. avg_daily_km
3. load_factor

Total mileage and age show little separation between the two groups,
so they are not used in the risk score.
"""

from pathlib import Path

import pandas as pd


HISTORY_FILE = Path("fleet_history.csv")

RISK_COLUMNS = [
    "km_since_service",
    "avg_daily_km",
    "load_factor",
]


def compare_groups(df: pd.DataFrame) -> pd.DataFrame:
    """Compare feature averages for broken-down and healthy cars."""
    grouped = df.groupby("broke_down")[RISK_COLUMNS + [
        "odometer_km",
        "age_years",
    ]].mean()

    return grouped


def calculate_risk(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate a simple 0-100 breakdown risk score."""
    result = df.copy()

    scores = []

    for column in RISK_COLUMNS:
        minimum = result[column].min()
        maximum = result[column].max()

        if maximum == minimum:
            normalized = pd.Series(0.0, index=result.index)
        else:
            normalized = (
                (result[column] - minimum)
                / (maximum - minimum)
            )

        scores.append(normalized)

    result["risk_score"] = (
        scores[0] * 0.5
        + scores[1] * 0.3
        + scores[2] * 0.2
    ) * 100

    return result.sort_values(
        "risk_score",
        ascending=False,
    )


def main() -> None:
    """Load fleet history, explain the important factors, and rank risk."""
    df = pd.read_csv(HISTORY_FILE)

    grouped = compare_groups(df)

    broken = grouped.loc[1]
    healthy = grouped.loc[0]

    print("BREAKDOWN-RISK ANALYSIS")
    print("=" * 60)

    print(
        "The strongest factors are km_since_service, "
        "avg_daily_km, and load_factor."
    )
    print(
        "Odometer mileage and age show little group separation, "
        "so they are not used in the risk score."
    )

    print("\nGROUP COMPARISON")
    print("-" * 60)

    for column in [
        "odometer_km",
        "age_years",
        "km_since_service",
        "avg_daily_km",
        "load_factor",
    ]:
        print(
            f"{column:20} "
            f"broke down={broken[column]:8.2f} "
            f"kept going={healthy[column]:8.2f}"
        )

    ranked = calculate_risk(df)

    print("\nTOP 20 CARS BY RISK")
    print("-" * 60)

    print(
        ranked[
            [
                "car_id",
                "risk_score",
                "km_since_service",
                "avg_daily_km",
                "load_factor",
                "broke_down",
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
