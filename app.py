import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")

# ----------------------
# CUSTOM STYLING
# ----------------------
st.markdown("""
    <style>
        .stApp {
            background-color: #e6f2ff;
        }
        .title-style {
            color: #0b3d91;
            font-size: 40px;
            font-weight: bold;
        }
        .kpi-box {
            border: 3px solid black;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            font-weight: bold;
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# TITLE
# ----------------------
st.markdown('<p class="title-style">Expense Tracker Dashboard</p>', unsafe_allow_html=True)

# ----------------------
# FILE UPLOAD
# ----------------------
uploaded_file = st.file_uploader("Upload your expense CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    # ----------------------
    # KPIs CALCULATIONS
    # ----------------------
    total_spent = df["Amount"].sum()
    highest_category = df.groupby("Category")["Amount"].sum().idxmax()
    highest_category_value = df.groupby("Category")["Amount"].sum().max()
    avg_transaction = df["Amount"].mean()

    # ----------------------
    # KPI DISPLAY (HORIZONTAL)
    # ----------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="kpi-box">
                Total Spent <br>
                ${total_spent:,.2f}
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="kpi-box">
                Highest Category <br>
                {highest_category} <br>
                ${highest_category_value:,.2f}
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="kpi-box">
                Avg Transaction <br>
                ${avg_transaction:,.2f}
            </div>
        """, unsafe_allow_html=True)

    st.write("")

    # ----------------------
    # BAR CHART (AFTER KPIs)
    # ----------------------
    monthly = df.groupby("Month")["Amount"].sum()
    monthly.index = monthly.index.strftime("%b")

    st.subheader("Monthly Expense Summary")

    fig, ax = plt.subplots()
    ax.bar(monthly.index, monthly.values)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Expenses")

    st.pyplot(fig)

    # ----------------------
    # SMART CATEGORY QUIZ
    # ----------------------
    st.subheader("Expense Awareness Check")

    category_choice = st.selectbox(
        "Which category should we reduce spending on?",
        df["Category"].unique()
    )

    if st.button("Submit Choice"):
        if category_choice == highest_category:
            st.success("✅ Correct! This is your highest spending category! 💰🔥")
        else:
            st.error("❌ Not quite. Review your highest category and try again!")
