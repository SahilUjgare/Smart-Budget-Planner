# 💰 Smart Budget Planner

A Streamlit web app that takes a person's monthly income and expenses and generates a personalized budget plan using the **50/30/20 rule** (or a custom allocation), along with visual breakdowns and actionable savings insights.

## Features
- Input monthly salary + other income in multiple currencies
- Choose between the 50/30/20 rule or a fully custom Needs/Wants/Savings split
- Enter actual expenses across 11 categories (rent, groceries, transport, dining, entertainment, etc.)
- Recommended vs. Actual spending comparison chart
- Interactive pie chart of spending distribution
- Auto-generated personalized insights (overspending alerts, savings gap, emergency fund target)
- Downloadable plain-text budget report

## Tech Stack
- Python
- Streamlit
- Plotly
- Pandas

## Run Locally
```bash
git clone https://github.com/SahilUjgare/smart-budget-planner.git
cd smart-budget-planner
pip install -r requirements.txt
streamlit run budget_planner_app.py
```

## requirements.txt
```
streamlit
plotly
pandas
```



## Author
Sahil Ujgare — [GitHub](https://github.com/SahilUjgare) | [LinkedIn](https://linkedin.com/in/sahil-ujgare-225866267)
