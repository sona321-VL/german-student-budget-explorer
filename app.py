
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="German Student Budget Explorer",
    page_icon="🇩🇪",
    layout="wide"
)

st.title("🇩🇪 German Student Budget Explorer")
st.write(
    "Estimate and compare monthly living expenses "
    "for students in German cities."
)

# Illustrative sample data in euros per month
data = {
    "City": ["Berlin", "Munich", "Hamburg", "Aachen"],
    "Rent": [450, 650, 500, 400],
    "Food": [250, 280, 250, 230],
    "Transport": [50, 60, 55, 50],
    "Health Insurance": [140, 140, 140, 140],
    "Phone": [15, 15, 15, 15],
    "Personal Expenses": [100, 120, 100, 90]
}

df = pd.DataFrame(data)

expense_columns = [
    "Rent",
    "Food",
    "Transport",
    "Health Insurance",
    "Phone",
    "Personal Expenses"
]

df["Total Monthly Expenses"] = df[expense_columns].sum(axis=1)

# User inputs
st.sidebar.header("Your Budget")

city = st.sidebar.selectbox(
    "Choose a German city",
    df["City"]
)

monthly_budget = st.sidebar.number_input(
    "Your monthly budget (€)",
    min_value=0,
    value=1200,
    step=50
)

# Selected city data
selected = df[df["City"] == city].iloc[0]
expenses = selected["Total Monthly Expenses"]
remaining = monthly_budget - expenses

# Display results
st.subheader(f"Your estimated budget in {city}")

col1, col2, col3 = st.columns(3)

col1.metric("Estimated expenses", f"€{expenses:,.0f}")
col2.metric("Your budget", f"€{monthly_budget:,.0f}")
col3.metric("Money remaining", f"€{remaining:,.0f}")

if remaining >= 0:
    st.success("Your example budget covers the estimated expenses.")
else:
    st.warning("Your example budget is below the estimated expenses.")

st.subheader("Monthly expense breakdown")

breakdown = selected[expense_columns].sort_values(
    ascending=False
)

st.bar_chart(breakdown)

st.caption(
    "Educational prototype: expense values are illustrative, "
    "not verified current living costs. Actual costs vary by "
    "housing, insurance, transport and individual circumstances."
)

st.subheader("Compare all cities")

st.dataframe(
    df[["City"] + expense_columns + ["Total Monthly Expenses"]],
    hide_index=True,
    use_container_width=True
)


# Compare total monthly expenses across cities

st.subheader("Monthly Cost Comparison Across Cities")

city_comparison = df.set_index("City")[
    ["Total Monthly Expenses"]
].sort_values(
    by="Total Monthly Expenses",
    ascending=False
)

st.bar_chart(city_comparison)

st.subheader("Which city is the most affordable?")

cheapest_city = df.loc[
    df["Total Monthly Expenses"].idxmin()
]

st.write(
    f"Based on our sample data, {cheapest_city['City']} "
    f"has the lowest estimated monthly expenses: "
    f"€{cheapest_city['Total Monthly Expenses']:,.0f}."
)
