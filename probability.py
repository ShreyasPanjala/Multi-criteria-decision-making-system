"""Expected utility calculation using a simple risk-adjustment model."""
from __future__ import annotations


def calculate_expected_utility(utility_score: float, risk_score: float) -> float:
    """Reduce utility by estimated risk and return the risk-adjusted score."""
    success_probability = max(0.0, min(1.0, (10 - risk_score) / 10))
    expected_utility = utility_score * success_probability
    return round(expected_utility, 2)
