
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Nassau Candy Shipping & Profitability")
st.write(
    "Explore shipping performance, sales, and profitability "
    "using your own dataset."
)

uploaded_file = st.file_uploader(
    "Upload the Nassau Candy CSV dataset",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required = [
            "Order ID", "Sales", "Gross Profit",
            "Cost", "Ship Mode", "Order Date", "Ship Date"
        ]

        missing = [col for col in required if col not in df.columns]

        if missing:
            st.error("Missing required columns: " + ", ".join(missing))
        else:
            df["Order Date"] = pd.to_datetime(
                df["Order Date"], errors="coerce"
            )
            df["Ship Date"] = pd.to_datetime(
                df["Ship Date"], errors="coerce"
            )

            df["Shipping Days"] = (
                df["Ship Date"] - df["Order Date"]
            ).dt.days

            st.subheader("Business overview")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Unique Orders", f"{df['Order ID'].nunique():,}")
            c2.metric("Total Sales", f"{df['Sales'].sum():,.2f}")
            c3.metric("Gross Profit", f"{df['Gross Profit'].sum():,.2f}")

            margin = (
                df["Gross Profit"].sum() / df["Sales"].sum() * 100
                if df["Sales"].sum() != 0 else 0
            )
            c4.metric("Gross Profit Margin", f"{margin:.2f}%")

            st.subheader("Shipping performance")

            shipping = (
                df.dropna(subset=["Shipping Days"])
                .groupby("Ship Mode")["Shipping Days"]
                .mean()
                .sort_values()
            )

            st.bar_chart(shipping)

            st.subheader("Profitability by region")

            if "Region" in df.columns:
                regional_profit = (
                    df.groupby("Region")["Gross Profit"]
                    .sum()
                    .sort_values(ascending=False)
                )
                st.bar_chart(regional_profit)

            st.subheader("Dataset preview")
            st.dataframe(df.head(20), use_container_width=True)

            st.caption(
                "Shipping Days measures order-to-ship time, "
                "not necessarily delivery time. Factory-level "
                "optimization requires additional factory data."
            )

    except Exception as e:
        st.error(f"Unable to read this CSV: {e}")

else:
    st.info("Upload your CSV file to view the dashboard.")
