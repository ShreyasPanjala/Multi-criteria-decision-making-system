"""Streamlit UI for the AI-based job selection system."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from constraints import filter_jobs
from explain import explain_job
from jobs_data import load_jobs
from probability import calculate_expected_utility
from search import astar_search, bfs_search, dfs_search, ucs_search
from utility import calculate_utility


st.set_page_config(page_title="AI Job Selection System", layout="wide")

st.title("AI-Based Multi-Criteria Job Selection Decision Support System")
st.caption("Uses the uploaded ds_salaries.csv dataset and risk-adjusted utility scoring.")


@st.cache_data
def get_jobs() -> list[dict]:
    return load_jobs()


jobs = get_jobs()

min_dataset_salary = int(min(job["salary_usd"] for job in jobs))
max_dataset_salary = int(max(job["salary_usd"] for job in jobs))
default_salary = int(pd.Series([job["salary_usd"] for job in jobs]).median())

st.sidebar.header("User Preferences")

min_salary_usd = st.sidebar.slider(
    "Minimum Salary (USD)",
    min_value=min_dataset_salary,
    max_value=max_dataset_salary,
    value=default_salary,
    step=5000,
)

locations = ["Any"] + sorted({job["company_location"] for job in jobs})
preferred_location = st.sidebar.selectbox("Preferred Company Location", locations)

remote_only = st.sidebar.checkbox("Remote Only")

experience_options = ["Any", "EN", "MI", "SE", "EX"]
experience_level = st.sidebar.selectbox(
    "Experience Level",
    experience_options,
    format_func=lambda value: {
        "Any": "Any",
        "EN": "Entry-level",
        "MI": "Mid-level",
        "SE": "Senior-level",
        "EX": "Executive-level",
    }.get(value, value),
)

st.sidebar.header("Utility Weights")

salary_weight = st.sidebar.slider("Salary Importance", 0.0, 1.0, 0.4, 0.05)
work_life_balance_weight = st.sidebar.slider(
    "Work-Life Balance Importance", 0.0, 1.0, 0.3, 0.05
)
growth_weight = st.sidebar.slider("Growth Importance", 0.0, 1.0, 0.3, 0.05)

algorithm = st.sidebar.selectbox("Choose Ranking Strategy", ["BFS", "DFS", "UCS", "A*"])

filtered_jobs = filter_jobs(
    jobs=jobs,
    min_salary_usd=min_salary_usd,
    preferred_location=preferred_location,
    remote_only=remote_only,
    experience_level=experience_level,
)

scored_jobs = []
for job in filtered_jobs:
    scored_job = job.copy()
    scored_job["utility_score"] = calculate_utility(
        scored_job,
        salary_weight=salary_weight,
        work_life_balance_weight=work_life_balance_weight,
        growth_weight=growth_weight,
    )
    scored_job["expected_utility_score"] = calculate_expected_utility(
        scored_job["utility_score"], scored_job["risk_score"]
    )
    scored_jobs.append(scored_job)

if algorithm == "BFS":
    ranked_jobs = bfs_search(scored_jobs)
elif algorithm == "DFS":
    ranked_jobs = dfs_search(scored_jobs)
elif algorithm == "UCS":
    ranked_jobs = ucs_search(scored_jobs)
else:
    ranked_jobs = astar_search(scored_jobs)

st.header("Recommended Jobs")

if not ranked_jobs:
    st.error("No jobs match your constraints. Try lowering the salary or widening filters.")
    st.stop()

best_job = ranked_jobs[0]
st.success(
    f"Best Recommended Job: {best_job['job_title']} — {best_job['company_location']} "
    f"({best_job['remote_type']})"
)

summary_df = pd.DataFrame(ranked_jobs[:20])[
    [
        "job_title",
        "salary_usd",
        "experience_level_name",
        "company_location",
        "remote_type",
        "company_size_name",
        "work_life_balance_score",
        "growth_score",
        "risk_score",
        "utility_score",
        "expected_utility_score",
    ]
]

summary_df = summary_df.rename(
    columns={
        "job_title": "Job Title",
        "salary_usd": "Salary USD",
        "experience_level_name": "Experience",
        "company_location": "Location",
        "remote_type": "Work Mode",
        "company_size_name": "Company Size",
        "work_life_balance_score": "WLB",
        "growth_score": "Growth",
        "risk_score": "Risk",
        "utility_score": "Utility",
        "expected_utility_score": "Expected Utility",
    }
)

st.dataframe(summary_df, use_container_width=True, hide_index=True)

st.subheader("Explanations")
for index, job in enumerate(ranked_jobs[:10], start=1):
    with st.expander(f"#{index}: {job['job_title']} — {job['company_location']}"):
        st.write(explain_job(job))

st.header("Expected Utility Comparison")
chart_df = pd.DataFrame(ranked_jobs[:10])[ ["job_title", "expected_utility_score"] ]
chart_df = chart_df.set_index("job_title")
st.bar_chart(chart_df)
