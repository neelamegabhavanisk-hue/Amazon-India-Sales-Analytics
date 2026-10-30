from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Amazon India Sales Analytics",
    page_icon="📈",
    layout="wide",
)


def format_currency(value: float) -> str:
    return f"₹{value:,.0f}"


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            .main {
                background: linear-gradient(180deg, #f6f9ff 0%, #eef3ff 100%);
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
            }
            h1 {
                color: #1d3557;
                font-weight: 800;
                letter-spacing: -0.04em;
            }
            .stMetric > div {
                background: rgba(255,255,255,0.8);
                border: 1px solid rgba(29,53,87,0.08);
                border-radius: 16px;
                box-shadow: 0 10px 25px rgba(31, 41, 55, 0.06);
                padding: 1rem 1.25rem;
            }
            .stSidebar {
                background: #f8fbff;
            }
            .section-header {
                color: #1d3557;
                font-size: 1.25rem;
                font-weight: 700;
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
            }
            .insight-box {
                background: linear-gradient(135deg, #ffffff, #edf5ff);
                border-left: 5px solid #4c78ff;
                padding: 1rem 1.1rem;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(76,120,255,0.08);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv("data/amazon_india_sales_analytics.csv")


def main() -> None:
    apply_theme()
    df = load_data().copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month_name"] = df["date"].dt.month_name()

    st.title("Amazon India: Sales Analytics Dashboard 📈🇮🇳")
    st.caption("Executive view of customer demand, revenue growth, and operational efficiency from 2014 to 2023")

    with st.sidebar:
        st.header("Filters")
        years = sorted(df["year"].unique())
        selected_years = st.multiselect("Year", years, default=years)

        regions = sorted(df["region"].unique())
        selected_regions = st.multiselect("Region", regions, default=regions)

        categories = sorted(df["category"].unique())
        selected_categories = st.multiselect("Category", categories, default=categories)

        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        selected_months = st.multiselect("Month", months, default=months)

        st.markdown("---")
        st.caption("Portfolio project goal: measure regional scale, category contribution, and operating health across a decade of Amazon India trade activity.")

    filtered = df[
        df["year"].isin(selected_years)
        & df["region"].isin(selected_regions)
        & df["category"].isin(selected_categories)
        & df["month_name"].isin(selected_months)
    ].copy()

    if filtered.empty:
        st.warning("No data matches the current filters. Please broaden the selection.")
        return

    revenue_by_year = (
        filtered.groupby("year", as_index=False)["net_revenue"].sum().sort_values("year")
    )
    revenue_by_region = (
        filtered.groupby("region", as_index=False)["net_revenue"].sum().sort_values("net_revenue", ascending=False)
    )
    revenue_by_category = (
        filtered.groupby("category", as_index=False)["net_revenue"].sum().sort_values("net_revenue", ascending=False)
    )
    monthly_summary = (
        filtered.groupby("month_name", as_index=False)["net_revenue"].sum().sort_values("net_revenue", ascending=False)
    )

    total_revenue = filtered["net_revenue"].sum()
    total_orders = filtered["orders"].sum()
    avg_rating = filtered["customer_rating"].mean()
    avg_delivery = filtered["delivery_days"].mean()
    return_rate = (filtered["returns"].sum() / filtered["orders"].sum()) * 100
    avg_discount = filtered["discount_pct"].mean()

    if len(revenue_by_year) > 1:
        latest = float(revenue_by_year["net_revenue"].iloc[-1])
        previous = float(revenue_by_year["net_revenue"].iloc[-2])
        yoy_growth = ((latest - previous) / previous) * 100 if previous else 0.0
    else:
        yoy_growth = 0.0

    top_region = revenue_by_region.iloc[0]["region"]
    top_category = revenue_by_category.iloc[0]["category"]
    peak_month = monthly_summary.iloc[0]["month_name"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Net Revenue", format_currency(total_revenue), f"{yoy_growth:.1f}% YoY")
    col2.metric("Orders", f"{total_orders:,.0f}", "")
    col3.metric("Avg. Rating", f"{avg_rating:.2f}/5", f"{avg_discount:.1f}% avg discount")
    col4.metric("Return Rate", f"{return_rate:.2f}%", f"{avg_delivery:.1f} days avg delivery")

    st.markdown('<div class="section-header">Executive summary</div>', unsafe_allow_html=True)
    insights_col1, insights_col2, insights_col3 = st.columns(3)
    with insights_col1:
        st.markdown(
            f"""
            <div class="insight-box">
                <b>Top revenue region</b><br>
                {top_region} is leading the current portfolio with the highest net revenue contribution.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with insights_col2:
        st.markdown(
            f"""
            <div class="insight-box">
                <b>Top category</b><br>
                {top_category} is the strongest category driver, making diversified demand more resilient.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with insights_col3:
        st.markdown(
            f"""
            <div class="insight-box">
                <b>Peak demand period</b><br>
                {peak_month} stands out as the strongest revenue month across the selected time window.
            </div>
            """,
            unsafe_allow_html=True,
        )

    overview_tab, deep_dive_tab, data_tab = st.tabs(["Overview", "Performance Deep Dive", "Raw Data"])

    with overview_tab:
        fig_trend = px.line(
            revenue_by_year,
            x="year",
            y="net_revenue",
            markers=True,
            line_shape="spline",
            title="Annual net revenue trend",
            labels={"year": "Year", "net_revenue": "Net revenue (₹)"},
            template="plotly_white",
        )
        fig_trend.update_traces(line=dict(color="#4c78ff", width=3), marker=dict(size=8, color="#1d3557"))
        fig_trend.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig_trend, width="stretch")

        left_col, right_col = st.columns(2)

        fig_region = px.bar(
            revenue_by_region,
            x="region",
            y="net_revenue",
            color="region",
            title="Net revenue by region",
            labels={"region": "Region", "net_revenue": "Net revenue (₹)"},
            template="plotly_white",
            color_discrete_sequence=px.colors.sequential.Blues_r,
        )
        fig_region.update_layout(showlegend=False, margin=dict(l=10, r=10, t=50, b=10))
        left_col.plotly_chart(fig_region, width="stretch")

        fig_category = px.pie(
            revenue_by_category,
            names="category",
            values="net_revenue",
            title="Revenue share by category",
            template="plotly_white",
        )
        fig_category.update_traces(textposition="inside", textinfo="percent+label")
        right_col.plotly_chart(fig_category, width="stretch")

    with deep_dive_tab:
        monthly_chart = px.bar(
            monthly_summary,
            x="month_name",
            y="net_revenue",
            color="net_revenue",
            title="Revenue by month",
            labels={"month_name": "Month", "net_revenue": "Net revenue (₹)"},
            template="plotly_white",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(monthly_chart, width="stretch")

        region_cat = (
            filtered.groupby(["region", "category"], as_index=False)["net_revenue"].sum()
            .sort_values("net_revenue", ascending=False)
        )
        category_region = px.bar(
            region_cat,
            x="category",
            y="net_revenue",
            color="region",
            title="Category revenue by region",
            labels={"category": "Category", "net_revenue": "Net revenue (₹)"},
            template="plotly_white",
            barmode="group",
        )
        st.plotly_chart(category_region, width="stretch")

    with data_tab:
        display_columns = [
            "year",
            "month_name",
            "region",
            "category",
            "orders",
            "revenue",
            "net_revenue",
            "returns",
            "discount_pct",
            "customer_rating",
            "delivery_days",
        ]
        st.dataframe(
            filtered[display_columns].sort_values(["year", "month_name", "region"]).reset_index(drop=True),
            width="stretch",
        )


if __name__ == "__main__":
    main()
