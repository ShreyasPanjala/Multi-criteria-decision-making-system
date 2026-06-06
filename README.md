# AI Job Selection System - Fixed Version

This corrected version uses the uploaded `ds_salaries.csv` schema directly and fixes the broken naming mismatches in the original files.

## Main fixes

- Replaced inconsistent keys such as `salary`, `location`, `company`, `wlb`, `growth`, and `risk` with clearer names:
  - `salary_usd`
  - `company_location`
  - `remote_type`
  - `experience_level`
  - `work_life_balance_score`
  - `growth_score`
  - `risk_score`
  - `utility_score`
  - `expected_utility_score`
- Fixed `filter_jobs()` so it accepts and applies `experience_level`.
- Added `remote_type` from the dataset's `remote_ratio` column.
- Removed the fake `company` field because the uploaded dataset does not contain company names.
- Removed `print(df.columns)` debug output.
- Added dataset validation with clear missing-column errors.
- Normalized salary into `salary_score` so salary does not overpower the other 0-10 scores.
- Added a Flask fallback app in `flask_app.py`.

## Run with Streamlit

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Run with Flask fallback

```bash
pip install -r requirements.txt
python flask_app.py
```

Then open the local URL printed by Flask, usually `http://127.0.0.1:5000`.
