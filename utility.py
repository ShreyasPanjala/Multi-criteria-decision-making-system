"""Utility score calculation for job records."""
from __future__ import annotations

from typing import Any


def calculate_utility(
    job: dict[str, Any],
    salary_weight: float,
    work_life_balance_weight: float,
    growth_weight: float,
) -> float:
    """Calculate a 0-10 utility score using normalized criteria.

    The dataset salary values are large USD numbers, while the other criteria are 0-10
    scores. Using salary_score keeps salary from overpowering every other factor.
    """
    total_weight = salary_weight + work_life_balance_weight + growth_weight
    if total_weight <= 0:
        salary_weight = work_life_balance_weight = growth_weight = 1 / 3
        total_weight = 1

    utility_score = (
        salary_weight * job["salary_score"]
        + work_life_balance_weight * job["work_life_balance_score"]
        + growth_weight * job["growth_score"]
    ) / total_weight

    return round(utility_score, 2)
