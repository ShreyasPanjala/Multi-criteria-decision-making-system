"""Flask fallback UI for the AI-based job selection system."""
from __future__ import annotations

import html

from flask import Flask, request, render_template_string

from constraints import filter_jobs
from explain import explain_job
from jobs_data import load_jobs
from probability import calculate_expected_utility
from search import astar_search, bfs_search, dfs_search, ucs_search
from utility import calculate_utility

app = Flask(__name__)


def rank_jobs(
    min_salary_usd: float,
    preferred_location: str,
    remote_only: bool,
    experience_level: str,
    salary_weight: float,
    work_life_balance_weight: float,
    growth_weight: float,
    algorithm: str,
) -> list[dict]:
    jobs = load_jobs()
    filtered_jobs = filter_jobs(
        jobs=jobs,
        min_salary_usd=min_salary_usd,
        preferred_location=preferred_location,
        remote_only=remote_only,
        experience_level=experience_level,
    )

    scored_jobs: list[dict] = []
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
        return bfs_search(scored_jobs)
    if algorithm == "DFS":
        return dfs_search(scored_jobs)
    if algorithm == "UCS":
        return ucs_search(scored_jobs)
    return astar_search(scored_jobs)


@app.route("/", methods=["GET", "POST"])
def index():
    jobs = load_jobs()
    locations = ["Any"] + sorted({job["company_location"] for job in jobs})
    salaries = [job["salary_usd"] for job in jobs]
    default_min_salary = int(sorted(salaries)[len(salaries) // 2])

    form = {
        "min_salary_usd": float(request.form.get("min_salary_usd", default_min_salary)),
        "preferred_location": request.form.get("preferred_location", "Any"),
        "remote_only": request.form.get("remote_only") == "on",
        "experience_level": request.form.get("experience_level", "Any"),
        "salary_weight": float(request.form.get("salary_weight", 0.4)),
        "work_life_balance_weight": float(request.form.get("work_life_balance_weight", 0.3)),
        "growth_weight": float(request.form.get("growth_weight", 0.3)),
        "algorithm": request.form.get("algorithm", "A*"),
    }

    ranked_jobs = rank_jobs(**form)
    top_jobs = ranked_jobs[:20]

    return render_template_string(
        TEMPLATE,
        locations=locations,
        top_jobs=top_jobs,
        form=form,
        explain_job=explain_job,
        html=html,
    )


TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Job Selection System</title>
  <style>
    body { margin: 0; font-family: Inter, Arial, sans-serif; background: #0f172a; color: #e5e7eb; }
    .page { display: grid; grid-template-columns: 320px 1fr; min-height: 100vh; }
    aside { background: #111827; padding: 24px; border-right: 1px solid #334155; }
    main { padding: 32px; }
    h1 { margin-top: 0; font-size: 30px; }
    label { display: block; margin-top: 16px; font-weight: 700; }
    input, select { width: 100%; box-sizing: border-box; margin-top: 6px; padding: 10px; border: 1px solid #475569; border-radius: 10px; background: #020617; color: #e5e7eb; }
    button { width: 100%; margin-top: 24px; padding: 12px; border: 0; border-radius: 12px; background: #38bdf8; color: #082f49; font-weight: 800; cursor: pointer; }
    table { width: 100%; border-collapse: collapse; background: #111827; border-radius: 14px; overflow: hidden; }
    th, td { padding: 12px; border-bottom: 1px solid #334155; text-align: left; vertical-align: top; }
    th { background: #1e293b; }
    .card { margin-bottom: 20px; padding: 18px; border-radius: 16px; background: #111827; border: 1px solid #334155; }
    .best { border-color: #38bdf8; box-shadow: 0 0 24px rgba(56,189,248,.15); }
    .muted { color: #94a3b8; }
  </style>
</head>
<body>
<div class="page">
  <aside>
    <h2>Filters</h2>
    <form method="post">
      <label>Minimum Salary USD</label>
      <input type="number" name="min_salary_usd" step="1000" value="{{ form.min_salary_usd|int }}">

      <label>Preferred Company Location</label>
      <select name="preferred_location">
        {% for location in locations %}
          <option value="{{ location }}" {% if form.preferred_location == location %}selected{% endif %}>{{ location }}</option>
        {% endfor %}
      </select>

      <label>Experience Level</label>
      <select name="experience_level">
        {% for code, label in [("Any", "Any"), ("EN", "Entry-level"), ("MI", "Mid-level"), ("SE", "Senior-level"), ("EX", "Executive-level")] %}
          <option value="{{ code }}" {% if form.experience_level == code %}selected{% endif %}>{{ label }}</option>
        {% endfor %}
      </select>

      <label><input style="width:auto" type="checkbox" name="remote_only" {% if form.remote_only %}checked{% endif %}> Remote Only</label>

      <h2>Weights</h2>
      <label>Salary Importance</label>
      <input type="number" name="salary_weight" min="0" max="1" step="0.05" value="{{ form.salary_weight }}">

      <label>Work-Life Balance Importance</label>
      <input type="number" name="work_life_balance_weight" min="0" max="1" step="0.05" value="{{ form.work_life_balance_weight }}">

      <label>Growth Importance</label>
      <input type="number" name="growth_weight" min="0" max="1" step="0.05" value="{{ form.growth_weight }}">

      <label>Ranking Strategy</label>
      <select name="algorithm">
        {% for algorithm in ["BFS", "DFS", "UCS", "A*"] %}
          <option value="{{ algorithm }}" {% if form.algorithm == algorithm %}selected{% endif %}>{{ algorithm }}</option>
        {% endfor %}
      </select>

      <button type="submit">Find Best Jobs</button>
    </form>
  </aside>

  <main>
    <h1>AI-Based Multi-Criteria Job Selection Decision Support System</h1>
    <p class="muted">Flask fallback version using the uploaded ds_salaries.csv dataset.</p>

    {% if top_jobs %}
      <div class="card best">
        <h2>Best Recommended Job: {{ top_jobs[0].job_title }}</h2>
        <p>{{ top_jobs[0].company_location }} · {{ top_jobs[0].remote_type }} · Expected Utility {{ top_jobs[0].expected_utility_score }}</p>
        <p>{{ explain_job(top_jobs[0]) }}</p>
      </div>

      <table>
        <thead>
          <tr>
            <th>Job Title</th><th>Salary USD</th><th>Experience</th><th>Location</th><th>Mode</th><th>WLB</th><th>Growth</th><th>Risk</th><th>Utility</th><th>Expected Utility</th>
          </tr>
        </thead>
        <tbody>
          {% for job in top_jobs %}
            <tr>
              <td>{{ job.job_title }}</td>
              <td>{{ "{:,.0f}".format(job.salary_usd) }}</td>
              <td>{{ job.experience_level_name }}</td>
              <td>{{ job.company_location }}</td>
              <td>{{ job.remote_type }}</td>
              <td>{{ job.work_life_balance_score }}</td>
              <td>{{ job.growth_score }}</td>
              <td>{{ job.risk_score }}</td>
              <td>{{ job.utility_score }}</td>
              <td>{{ job.expected_utility_score }}</td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    {% else %}
      <div class="card"><h2>No jobs match your constraints.</h2><p>Try lowering the salary or widening filters.</p></div>
    {% endif %}
  </main>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
