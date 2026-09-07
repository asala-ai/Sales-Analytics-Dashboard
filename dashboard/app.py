import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import kagglehub


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================
# Load Dataset
# =========================

@st.cache_data
def load_data():

    path = kagglehub.dataset_download(
        "binib1997/superstore"
    )

    df = pd.read_csv(
        path + "/Superstore.csv",
        encoding="latin1"
    )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"]
    )

    df["Year"] = df["Order Date"].dt.year

    df["Month"] = df["Order Date"].dt.month

    df["Month Name"] = df["Order Date"].dt.month_name()

    return df


df = load_data()


# =========================
# Dashboard Title
# =========================

st.title("📊 Sales Analytics Dashboard")

st.markdown(
"""
Interactive dashboard analyzing:

- Sales Performance
- Profitability
- Customer Segments
- Regional Performance
- Product Insights
"""
)


# =========================
# Filters
# =========================

st.sidebar.header("Dashboard Filters")


year_filter = st.sidebar.multiselect(
    "Select Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)


category_filter = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)


region_filter = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)


filtered_df = df[
    (df["Year"].isin(year_filter)) &
    (df["Category"].isin(category_filter)) &
    (df["Region"].isin(region_filter))
]


# =========================
# KPI Cards
# =========================

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

profit_margin = (
    total_profit / total_sales * 100
)

total_orders = filtered_df["Order ID"].nunique()

total_customers = filtered_df["Customer ID"].nunique()


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

col4.metric(
    "Orders",
    total_orders
)

col5.metric(
    "Customers",
    total_customers
)



# =========================
# Sales by Category
# =========================

st.subheader("Sales by Category")


category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
)


fig, ax = plt.subplots(figsize=(8,4))


category_sales.plot(
    kind="bar",
    ax=ax
)


ax.set_title(
    "Total Sales by Category"
)

ax.set_xlabel(
    "Category"
)

ax.set_ylabel(
    "Sales ($)"
)

plt.xticks(rotation=0)

plt.tight_layout()

st.pyplot(fig)



# =========================
# Sales Trend
# =========================

st.subheader("Monthly Sales Trend")


monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
)


fig, ax = plt.subplots(figsize=(8,4))


ax.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)


ax.set_title(
    "Monthly Sales Trend"
)

ax.set_xlabel(
    "Month"
)

ax.set_ylabel(
    "Sales ($)"
)


plt.grid(alpha=0.3)

st.pyplot(fig)



# =========================
# Profit by Category
# =========================

st.subheader("Profit by Category")


category_profit = (
    filtered_df.groupby("Category")["Profit"]
    .sum()
)


fig, ax = plt.subplots(figsize=(8,4))


category_profit.plot(
    kind="bar",
    ax=ax
)


ax.set_title(
    "Profit by Category"
)

ax.set_ylabel(
    "Profit ($)"
)

plt.xticks(rotation=0)

plt.tight_layout()

st.pyplot(fig)



# =========================
# Regional Analysis
# =========================

st.subheader("Regional Sales Performance")


region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
)


fig, ax = plt.subplots(figsize=(8,4))


region_sales.plot(
    kind="bar",
    ax=ax
)


ax.set_title(
    "Sales by Region"
)

ax.set_ylabel(
    "Sales ($)"
)

plt.xticks(rotation=0)

plt.tight_layout()

st.pyplot(fig)



# =========================
# Customer Segment
# =========================

st.subheader("Customer Segment Performance")


segment_analysis = (
    filtered_df.groupby("Segment")[["Sales","Profit"]]
    .sum()
)


st.dataframe(
    segment_analysis
)



# =========================
# Top Loss Products
# =========================

st.subheader("Top Loss-Making Products")


loss_products = (
    filtered_df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values()
    .head(10)
)


st.dataframe(
    loss_products
)
