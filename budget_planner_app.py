"""
Smart Budget Planner
---------------------
A Streamlit app that takes a person's monthly income and expenses,
then generates a personalized budget plan, savings recommendations,
and visual breakdowns.

Run locally:
    pip install streamlit plotly pandas
    streamlit run budget_planner_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ----------------------------- PAGE CONFIG -----------------------------
st.set_page_config(
    page_title="Smart Budget Planner",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Smart Budget Planner")
st.caption("Enter your income and expenses to get a personalized monthly budget plan.")

# ----------------------------- SIDEBAR: INCOME -----------------------------
st.sidebar.header("Step 1: Your Income")

currency = st.sidebar.selectbox("Currency", ["₹ INR", "$ USD", "€ EUR", "£ GBP", "AED"], index=0)
symbol = currency.split(" ")[0]

salary = st.sidebar.number_input(
    "Monthly Take-Home Salary", min_value=0.0, value=50000.0, step=1000.0
)
other_income = st.sidebar.number_input(
    "Other Monthly Income (freelance, rent, etc.)", min_value=0.0, value=0.0, step=500.0
)

total_income = salary + other_income
st.sidebar.markdown(f"**Total Monthly Income: {symbol}{total_income:,.0f}**")

# ----------------------------- SIDEBAR: BUDGET METHOD -----------------------------
st.sidebar.header("Step 2: Choose a Budgeting Method")

method = st.sidebar.radio(
    "Method",
    ["50/30/20 Rule (Recommended)", "Custom Allocation"],
)

if method == "50/30/20 Rule (Recommended)":
    needs_pct, wants_pct, savings_pct = 50, 30, 20
else:
    needs_pct = st.sidebar.slider("Needs %", 0, 100, 50)
    wants_pct = st.sidebar.slider("Wants %", 0, 100 - needs_pct, 30)
    savings_pct = 100 - needs_pct - wants_pct
    st.sidebar.write(f"Savings % (auto): **{savings_pct}%**")

# ----------------------------- MAIN: EXPENSES -----------------------------
st.header("Step 3: Enter Your Actual Monthly Expenses")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Needs (Essentials)")
    rent = st.number_input("Rent / Housing / EMI", min_value=0.0, value=15000.0, step=500.0)
    utilities = st.number_input("Utilities (Electricity, Water, Wifi)", min_value=0.0, value=2500.0, step=100.0)
    groceries = st.number_input("Groceries", min_value=0.0, value=5000.0, step=100.0)
    transport = st.number_input("Transportation / Fuel", min_value=0.0, value=3000.0, step=100.0)
    insurance = st.number_input("Insurance / Medical", min_value=0.0, value=1500.0, step=100.0)
    debt = st.number_input("Loan / Credit Card Payments", min_value=0.0, value=0.0, step=100.0)

with col2:
    st.subheader("Wants (Lifestyle)")
    dining = st.number_input("Dining Out / Food Delivery", min_value=0.0, value=3000.0, step=100.0)
    entertainment = st.number_input("Entertainment / Subscriptions", min_value=0.0, value=1500.0, step=100.0)
    shopping = st.number_input("Shopping / Personal Care", min_value=0.0, value=2000.0, step=100.0)
    travel = st.number_input("Travel / Weekend Trips", min_value=0.0, value=1000.0, step=100.0)
    misc = st.number_input("Miscellaneous", min_value=0.0, value=1000.0, step=100.0)

st.subheader("Current Savings / Investments")
current_savings = st.number_input(
    "Amount you currently save or invest each month", min_value=0.0, value=5000.0, step=100.0
)

# ----------------------------- CALCULATIONS -----------------------------
needs_total = rent + utilities + groceries + transport + insurance + debt
wants_total = dining + entertainment + shopping + travel + misc
actual_total_spent = needs_total + wants_total + current_savings
leftover = total_income - actual_total_spent

recommended_needs = total_income * needs_pct / 100
recommended_wants = total_income * wants_pct / 100
recommended_savings = total_income * savings_pct / 100

# ----------------------------- RESULTS -----------------------------
st.header("📊 Your Budget Breakdown")

if total_income <= 0:
    st.warning("Please enter your income in the sidebar to see your budget plan.")
    st.stop()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Income", f"{symbol}{total_income:,.0f}")
m2.metric("Total Spent", f"{symbol}{actual_total_spent:,.0f}")
m3.metric("Leftover / Shortfall", f"{symbol}{leftover:,.0f}",
          delta=f"{leftover:,.0f}", delta_color="normal" if leftover >= 0 else "inverse")
m4.metric("Savings Rate", f"{(current_savings/total_income*100):.1f}%")

st.markdown("---")

# Comparison chart: Recommended vs Actual
comparison_df = pd.DataFrame({
    "Category": ["Needs", "Wants", "Savings"],
    "Recommended": [recommended_needs, recommended_wants, recommended_savings],
    "Actual": [needs_total, wants_total, current_savings],
})

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Recommended vs Actual Allocation")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(name="Recommended", x=comparison_df["Category"], y=comparison_df["Recommended"]))
    fig_bar.add_trace(go.Bar(name="Actual", x=comparison_df["Category"], y=comparison_df["Actual"]))
    fig_bar.update_layout(barmode="group", yaxis_title=f"Amount ({symbol})")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    st.subheader("Where Your Money Actually Goes")
    expense_breakdown = pd.DataFrame({
        "Category": ["Rent/Housing", "Utilities", "Groceries", "Transport", "Insurance", "Debt",
                      "Dining Out", "Entertainment", "Shopping", "Travel", "Misc", "Savings"],
        "Amount": [rent, utilities, groceries, transport, insurance, debt,
                   dining, entertainment, shopping, travel, misc, current_savings],
    })
    expense_breakdown = expense_breakdown[expense_breakdown["Amount"] > 0]
    fig_pie = px.pie(expense_breakdown, names="Category", values="Amount", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# ----------------------------- INSIGHTS -----------------------------
st.header("🧠 Personalized Insights")

insights = []

if leftover < 0:
    insights.append(f"🔴 You're overspending by {symbol}{abs(leftover):,.0f} this month. Review your 'Wants' category first — it's usually the easiest to cut.")
elif leftover > 0:
    insights.append(f"🟢 You have {symbol}{leftover:,.0f} unallocated. Consider directing it to savings or an emergency fund.")

if needs_total > recommended_needs * 1.1:
    insights.append(f"⚠️ Your Needs spending ({symbol}{needs_total:,.0f}) is higher than the recommended {symbol}{recommended_needs:,.0f}. Rent/EMI is often the biggest lever here.")

if wants_total > recommended_wants * 1.1:
    insights.append(f"⚠️ Your Wants spending ({symbol}{wants_total:,.0f}) exceeds the recommended {symbol}{recommended_wants:,.0f}. Try trimming dining out or subscriptions.")

if current_savings < recommended_savings:
    gap = recommended_savings - current_savings
    insights.append(f"💡 You're saving {symbol}{gap:,.0f} less than the recommended {savings_pct}% target. Even a small automated transfer on payday helps build this habit.")
else:
    insights.append(f"✅ Great job — you're meeting or exceeding the recommended {savings_pct}% savings target!")

emergency_fund_target = needs_total * 6
insights.append(f"🏦 Emergency Fund Goal: Aim for {symbol}{emergency_fund_target:,.0f} (6 months of essential expenses) in a separate liquid savings account.")

for tip in insights:
    st.info(tip)

# ----------------------------- DOWNLOAD REPORT -----------------------------
st.header("📥 Download Your Budget Report")

report_lines = [
    "SMART BUDGET PLANNER REPORT",
    f"Generated on: {datetime.now().strftime('%d %B %Y')}",
    "-" * 40,
    f"Total Monthly Income: {symbol}{total_income:,.0f}",
    f"Budgeting Method: {method}",
    "",
    "RECOMMENDED ALLOCATION",
    f"  Needs ({needs_pct}%): {symbol}{recommended_needs:,.0f}",
    f"  Wants ({wants_pct}%): {symbol}{recommended_wants:,.0f}",
    f"  Savings ({savings_pct}%): {symbol}{recommended_savings:,.0f}",
    "",
    "ACTUAL SPENDING",
    f"  Needs: {symbol}{needs_total:,.0f}",
    f"  Wants: {symbol}{wants_total:,.0f}",
    f"  Savings: {symbol}{current_savings:,.0f}",
    f"  Leftover/Shortfall: {symbol}{leftover:,.0f}",
    "",
    "INSIGHTS",
] + [f"  - {tip}" for tip in insights]

report_text = "\n".join(report_lines)

st.download_button(
    label="Download Report (.txt)",
    data=report_text,
    file_name=f"budget_report_{datetime.now().strftime('%Y%m%d')}.txt",
    mime="text/plain",
)

st.markdown("---")
st.caption("Built with Streamlit • Data stays in your browser session only, nothing is stored.")
