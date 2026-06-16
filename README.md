# AI-Based Multi-Criteria Job Selection Decision Support System

## Overview

This project is an AI-based decision support system that recommends suitable jobs from the `ds_salaries.csv` dataset.
It allows users to filter jobs based on salary, location, remote work preference, and experience level. The system then calculates utility and expected utility scores to rank the best job options.

## Features

* Filter jobs by minimum salary, company location, remote work, and experience level
* Assign custom weights for salary, work-life balance, and growth
* Calculate utility score for each job
* Adjust recommendations using risk-based expected utility
* Rank jobs using BFS, DFS, UCS, and A* style strategies
* Display top recommended jobs with explanations
* Show expected utility comparison using a chart
* Includes both Streamlit UI and Flask fallback version

## Concepts Used

* Python data structures
* Constraint filtering
* BFS, DFS, UCS, and A* ranking strategies
* Utility-based decision making
* Expected utility under uncertainty
* Risk scoring
* Explainable AI recommendations

## Tech Stack

* Python
* Pandas
* Streamlit
* Flask

## Project Structure

```text
AI-Job-Selection-System/
│
├── app.py              # Streamlit main application
├── flask_app.py        # Flask fallback application
├── jobs_data.py        # Dataset loading and feature engineering
├── constraints.py      # Job filtering based on user constraints
├── utility.py          # Utility score calculation
├── probability.py      # Expected utility calculation
├── search.py           # BFS, DFS, UCS, and A* ranking strategies
├── explain.py          # Human-readable recommendation explanations
├── test_core.py        # Basic testing file
├── ds_salaries.csv     # Dataset
├── requirements.txt    # Required libraries
└── README.md
```

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run using Streamlit

```bash
streamlit run app.py
```

### 3. Run using Flask fallback

```bash
python flask_app.py
```

Then open the local URL shown in the terminal.

## Dataset

The project uses the `ds_salaries.csv` dataset.
Important columns used include:

* Job title
* Salary in USD
* Experience level
* Remote ratio
* Company location
* Company size

## Output

The system displays:

* Best recommended job
* Ranked job table
* Salary, work-life balance, growth, risk, utility, and expected utility scores
* Explanation for each recommendation
* Expected utility comparison chart

## Course Outcome Mapping

This project maps to the following AI course outcomes:

* **CO1:** Problem formulation using Python and data structures
* **CO2:** Use of BFS, DFS, UCS, and A* search strategies
* **CO3:** Constraint-based filtering
* **CO4:** Utility-based decision making
* **CO5:** Expected utility and uncertainty-aware reasoning
* **CO6:** Integrated AI pipeline with explainable output

## Conclusion

This project demonstrates how AI concepts can be applied to a real-world job recommendation problem.
It combines filtering, search strategies, utility scoring, risk adjustment, and explainable recommendations to support better decision making.

