import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Expense Analytics Dashboard", layout="wide")

# -----------------------------
# CUSTOM CSS (PORTFOLIO STYLE)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #eaf4ff;
}

.main-title {
    color: #0b3d91;
    font-size: 42px;
    font-weight: 700;
}

.kpi-card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
    text-align: center;
    font-weight: 600;
}

.kpi-value {
    font-size: 28px;
    margin-top: 10px;
}

.section-header {
    color: #0b3d91;
    font-size: 24px;
    font-weight: 600;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown('<p class="main-title">Expense Analytics Dashboard</p>', unsafe_allow_html=True)

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload your expense CSV file", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    # -----------------------------
    # SIDEBAR FILTERS
    # -----------------------------
    st.sidebar.header("Filter Data")

    selected_category = st.sidebar.multiselect(
        "Select Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    filtered_df = df[df["Category"].isin(selected_category)]

    # -----------------------------
    # KPI CALCULATIONS
    # -----------------------------
    total_spent = filtered_df["Amount"].sum()
    highest_category = filtered_df.groupby("Category")["Amount"].sum().idxmax()
    highest_value = filtered_df.groupby("Category")["Amount"].sum().max()
    avg_transaction = filtered_df["Amount"].mean()

    # -----------------------------
    # KPI DISPLAY
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            Total Spent
            <div class="kpi-value">${total_spent:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            Highest Category
            <div class="kpi-value">{highest_category}</div>
            ${highest_value:,.2f}
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            Avg Transaction
            <div class="kpi-value">${avg_transaction:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # MONTHLY TREND (LINE CHART)
    # -----------------------------
    st.markdown('<p class="section-header">Monthly Trend</p>', unsafe_allow_html=True)

    monthly = filtered_df.groupby("Month")["Amount"].sum()
    monthly.index = monthly.index.strftime("%b")

    fig1, ax1 = plt.subplots()
    ax1.plot(monthly.index, monthly.values, marker='o')
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Total Expenses")
    st.pyplot(fig1)

    # -----------------------------
    # CATEGORY BREAKDOWN (PIE)
    # -----------------------------
    st.markdown('<p class="section-header">Category Breakdown</p>', unsafe_allow_html=True)

    category_totals = filtered_df.groupby("Category")["Amount"].sum()

    fig2, ax2 = plt.subplots()
    ax2.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%')
    st.pyplot(fig2)

    # -----------------------------
    # DOWNLOAD BUTTON
    # -----------------------------
    st.download_button(
        label="Download Filtered Data",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_expenses.csv",
        mime="text/csv"
    )

    # -----------------------------
    # SMART QUIZ SECTION
    # -----------------------------
    st.markdown('<p class="section-header">Expense Optimization Challenge</p>', unsafe_allow_html=True)

    user_choice = st.selectbox(
        "Which category should we reduce spending on?",
        options=filtered_df["Category"].unique()
    )

    if st.button("Submit Answer"):
        if user_choice == highest_category:
            st.success("🎯 Excellent insight! This is your highest spending category. Smart financial awareness! 💡💰")
        else:
            st.warning("📊 Not the highest category. Review the dashboard and try again!")
