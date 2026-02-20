import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Expense Tracker Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your expense CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    # Monthly totals
    monthly = df.groupby("Month")["Amount"].sum()
    monthly.index = monthly.index.strftime("%b")

    st.subheader("Monthly Expense Summary")
    st.bar_chart(monthly)

    # Show raw data
    if st.checkbox("Show Raw Data"):
        st.dataframe(df)