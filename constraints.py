"""Filtering constraints for job records."""
from __future__ import annotations

from typing import Any


def filter_jobs(
    jobs: list[dict[str, Any]],
    min_salary_usd: float = 0,
    preferred_location: str = "Any",
    remote_only: bool = False,
    experience_level: str = "Any",
) -> list[dict[str, Any]]:
    """Return jobs that match the user's salary, location, remote, and experience filters."""
    filtered_jobs: list[dict[str, Any]] = []

    for job in jobs:
        if job["salary_usd"] < min_salary_usd:
            continue

        if preferred_location != "Any" and job["company_location"] != preferred_location:
            continue

        if remote_only and job["remote_type"] != "Remote":
            continue

        if experience_level != "Any" and job["experience_level"] != experience_level:
            continue

        filtered_jobs.append(job.copy())

    return filtered_jobs
