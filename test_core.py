from constraints import filter_jobs
from jobs_data import load_jobs
from probability import calculate_expected_utility
from search import astar_search, bfs_search, dfs_search, ucs_search
from utility import calculate_utility


def test_core_flow():
    jobs = load_jobs()
    assert jobs, "dataset should load at least one job"

    filtered = filter_jobs(
        jobs,
        min_salary_usd=50_000,
        preferred_location="Any",
        remote_only=False,
        experience_level="Any",
    )
    assert filtered, "filter should return jobs for broad constraints"

    scored = []
    for job in filtered[:20]:
        job = job.copy()
        job["utility_score"] = calculate_utility(job, 0.4, 0.3, 0.3)
        job["expected_utility_score"] = calculate_expected_utility(
            job["utility_score"], job["risk_score"]
        )
        scored.append(job)

    for strategy in (bfs_search, dfs_search, ucs_search, astar_search):
        ranked = strategy(scored)
        assert ranked, f"{strategy.__name__} should return ranked jobs"
        assert "job_title" in ranked[0]
        assert "expected_utility_score" in ranked[0]


if __name__ == "__main__":
    test_core_flow()
    print("All core tests passed.")
