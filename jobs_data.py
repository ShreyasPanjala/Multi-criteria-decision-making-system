"""Dataset loading and feature engineering for the job selection system."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


DATASET_COLUMNS = {
    "work_year",
    "experience_level",
    "employment_type",
    "job_title",
    "salary_in_usd",
    "remote_ratio",
    "company_location",
    "company_size",
}


REMOTE_TYPE_MAP = {
    0: "On-site",
    50: "Hybrid",
    100: "Remote",
}


EXPERIENCE_LEVEL_MAP = {
    "EN": "Entry-level",
    "MI": "Mid-level",
    "SE": "Senior-level",
    "EX": "Executive-level",
}


COMPANY_SIZE_MAP = {
    "S": "Small",
    "M": "Medium",
    "L": "Large",
}


def _dataset_path(csv_path: str | Path | None = None) -> Path:
    """Return the dataset path, defaulting to ds_salaries.csv beside this file."""
    if csv_path is not None:
        return Path(csv_path)
    return Path(__file__).resolve().parent / "ds_salaries.csv"


def _validate_dataset(df: pd.DataFrame) -> None:
    """Fail early with a clear message if the CSV is not the expected dataset."""
    missing_columns = sorted(DATASET_COLUMNS - set(df.columns))
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Dataset is missing required column(s): {missing}")


def _work_life_balance_score(remote_ratio: int) -> int:
    """Estimate work-life balance from remote work availability."""
    if remote_ratio >= 100:
        return 9
    if remote_ratio >= 50:
        return 7
    return 5


def _growth_and_risk_scores(company_size: str) -> tuple[int, int]:
    """Estimate growth and risk from company size."""
    if company_size == "L":
        return 9, 2
    if company_size == "M":
        return 7, 4
    return 5, 6


def load_jobs(csv_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load the salary dataset and convert rows into consistently named job records."""
    df = pd.read_csv(_dataset_path(csv_path))
    _validate_dataset(df)

    min_salary = float(df["salary_in_usd"].min())
    max_salary = float(df["salary_in_usd"].max())
    salary_range = max(max_salary - min_salary, 1.0)

    jobs: list[dict[str, Any]] = []

    for row_number, row in df.reset_index(drop=True).iterrows():
        salary_usd = float(row["salary_in_usd"])
        remote_ratio = int(row["remote_ratio"])
        company_size = str(row["company_size"])
        growth_score, risk_score = _growth_and_risk_scores(company_size)

        salary_score = 1 + ((salary_usd - min_salary) / salary_range) * 9

        jobs.append(
            {
                "job_id": int(row_number),
                "work_year": int(row["work_year"]),
                "job_title": str(row["job_title"]),
                "salary_usd": round(salary_usd, 2),
                "salary_score": round(salary_score, 2),
                "experience_level": str(row["experience_level"]),
                "experience_level_name": EXPERIENCE_LEVEL_MAP.get(
                    str(row["experience_level"]), str(row["experience_level"])
                ),
                "employment_type": str(row["employment_type"]),
                "remote_ratio": remote_ratio,
                "remote_type": REMOTE_TYPE_MAP.get(remote_ratio, "Unknown"),
                "company_location": str(row["company_location"]),
                "company_size": company_size,
                "company_size_name": COMPANY_SIZE_MAP.get(company_size, company_size),
                "work_life_balance_score": _work_life_balance_score(remote_ratio),
                "growth_score": growth_score,
                "risk_score": risk_score,
            }
        )

    return jobs
