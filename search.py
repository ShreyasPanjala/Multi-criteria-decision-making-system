"""Ranking strategies used by the UI.

These are simplified academic ranking strategies named after search algorithms. They
operate on the available job list rather than a graph, so each function returns jobs
ordered by the criterion that best represents that strategy in this project.
"""
from __future__ import annotations

from typing import Any


def bfs_search(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Breadth-first style: preserve dataset order after filtering."""
    return list(jobs)


def dfs_search(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Depth-first style: prioritize stronger career-growth paths."""
    return sorted(jobs, key=lambda job: job["growth_score"], reverse=True)


def ucs_search(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Uniform-cost style: prioritize lowest risk/cost first."""
    return sorted(jobs, key=lambda job: (job["risk_score"], -job["expected_utility_score"]))


def astar_search(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A* style: combine expected utility with a simple salary/growth heuristic."""
    ranked_jobs: list[dict[str, Any]] = []

    for job in jobs:
        ranked_job = job.copy()
        ranked_job["heuristic_score"] = round(
            ranked_job["expected_utility_score"]
            + 0.2 * ranked_job["salary_score"]
            + 0.2 * ranked_job["growth_score"]
            - 0.2 * ranked_job["risk_score"],
            2,
        )
        ranked_jobs.append(ranked_job)

    return sorted(ranked_jobs, key=lambda job: job["heuristic_score"], reverse=True)
