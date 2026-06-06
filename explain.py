"""Human-readable explanations for job recommendations."""
from __future__ import annotations

from typing import Any


def explain_job(job: dict[str, Any]) -> str:
    """Generate a clear explanation for why a job was ranked highly."""
    reasons: list[str] = []

    if job["salary_score"] >= 7:
        reasons.append("salary is strong compared with the uploaded dataset")
    elif job["salary_score"] >= 4:
        reasons.append("salary is reasonable compared with the uploaded dataset")
    else:
        reasons.append("salary is lower, but other factors may compensate")

    if job["work_life_balance_score"] >= 8:
        reasons.append("remote work availability improves work-life balance")
    elif job["work_life_balance_score"] >= 6:
        reasons.append("hybrid work gives moderate flexibility")
    else:
        reasons.append("on-site work gives a lower flexibility score")

    if job["growth_score"] >= 8:
        reasons.append("company size suggests stronger growth opportunities")
    else:
        reasons.append("growth score is moderate based on company size")

    if job["risk_score"] <= 3:
        reasons.append("risk is estimated to be low")
    elif job["risk_score"] <= 5:
        reasons.append("risk is estimated to be moderate")
    else:
        reasons.append("risk is estimated to be higher")

    return (
        f"{job['job_title']} in {job['company_location']} is recommended because "
        + "; ".join(reasons)
        + f". Utility: {job['utility_score']}, expected utility: {job['expected_utility_score']}."
    )
