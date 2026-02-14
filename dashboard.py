import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import urllib.parse
import streamlit as st

DB_USER = "postgres"
DB_PASSWORD = urllib.parse.quote_plus("Mahivalli@24")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "stockhost"
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

df = pd.read_csv("master_csv_with_sector.csv")
df["date"] = pd.to_datetime(df["date"])

pivot_df = df.pivot(index="date", columns="Ticker", values="close")
returns_df = pivot_df.pct_change().dropna()
cumulative_returns = (1 + returns_df).cumprod()

if "Sector" in df.columns:
    df["Year"] = df["date"].dt.year
    yearly_returns = df.groupby(["Ticker", "Sector", "Year"])["close"].apply(
        lambda x: x.iloc[-1] / x.iloc[0] - 1 if len(x) > 1 else None
    ).reset_index(name="YearlyReturn")
    sector_perf = yearly_returns.groupby(["Sector", "Year"])["YearlyReturn"].mean().reset_index()
else:
    sector_perf = None

corr_matrix = returns_df.corr()
corr_matrix_reset = corr_matrix.reset_index().rename(columns={"index": "Ticker"})
corr_matrix_reset.to_sql("correlation_matrix", engine, if_exists="replace", index=False)

df["YearMonth"] = df["date"].dt.to_period("M").astype(str)
monthly_returns = df.groupby(["Ticker", "YearMonth"])["close"].apply(
    lambda x: x.iloc[-1] / x.iloc[0] - 1 if len(x) > 1 else None
).reset_index(name="MonthlyReturn")

top_gainers = (
    monthly_returns.groupby("YearMonth", group_keys=False)
    .apply(lambda x: x.nlargest(5, "MonthlyReturn"))
    .reset_index(drop=True)
)
top_losers = (
    monthly_returns.groupby("YearMonth", group_keys=False)
    .apply(lambda x: x.nsmallest(5, "MonthlyReturn"))
    .reset_index(drop=True)
)
st.title("DATA DRIVEN STOCK STOCK ANALYSIS")
page = st.sidebar.radio("📂 Navigate", ["Front Page", "Correlation Analysis", "Monthly Gainers & Losers"])

if page == "Front Page":
    st.title("📊 Stock Analysis Dashboard")

    # Volatility
    volatility = returns_df.std().sort_values(ascending=False)
    top10_volatility = volatility.head(10)
    st.subheader("1️⃣ Top 10 Volatile Stocks")
    st.dataframe(top10_volatility)

    top10_volatility_df = top10_volatility.reset_index()
    top10_volatility_df.columns = ["Ticker", "Volatility"]
    st.bar_chart(top10_volatility_df.set_index("Ticker"))

    # Cumulative returns
    final_cumulative = cumulative_returns.iloc[-1].sort_values(ascending=False)
    top5_cumulative = final_cumulative.head(5).index.tolist()

    st.subheader("2️⃣ Cumulative Return Over Time (Top 5 Stocks)")
    st.line_chart(cumulative_returns[top5_cumulative])

    #st.subheader("📋 Final Cumulative Returns Table (Top 5 Stocks)")
    #cumulative_table = final_cumulative.loc[top5_cumulative].reset_index()
    #cumulative_table.columns = ["Ticker", "FinalCumulativeReturn"]
    #st.dataframe(cumulative_table)

    if sector_perf is not None and not sector_perf.empty:
        st.subheader("3️⃣ Sector-wise Yearly Returns")
        st.dataframe(sector_perf)

        st.subheader("📉 Sector-wise Yearly Returns (Bar Chart)")
        bar_data = sector_perf.pivot(index="Sector", columns="Year", values="YearlyReturn")
        st.bar_chart(bar_data)
    else:
        st.info("⚠️ No 'Sector' column found in master_csv_with_sector, skipping sector analysis.")

elif page == "Correlation Analysis":
    st.title("🔗 Correlation Analysis")

    st.subheader("📊 Correlation Matrix of Stock Returns")
    st.dataframe(corr_matrix)


    corr_pairs = (
        corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        .stack()
        .rename_axis(["Ticker1", "Ticker2"])
        .reset_index(name="Correlation")
    )
    top5_corr = corr_pairs.sort_values("Correlation", ascending=False).head(5)

    st.subheader("📈 Top 5 Highly Correlated Ticker Pairs")
    st.dataframe(top5_corr)

    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(
        top5_corr["Ticker1"] + " & " + top5_corr["Ticker2"],
        top5_corr["Correlation"],
        color="skyblue"
    )
    ax.set_title("Top 5 Highly Correlated Ticker Pairs")
    ax.set_ylabel("Correlation Coefficient")
    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig)

elif page == "Monthly Gainers & Losers":
    st.title("📈 Monthly Top 5 Gainers & Losers")

    selected_month = st.selectbox("Select Month", monthly_returns["YearMonth"].unique())
    
    gainers = top_gainers[top_gainers["YearMonth"] == selected_month]
    losers = top_losers[top_losers["YearMonth"] == selected_month]

    st.subheader(f"📅 {selected_month} — Top 5 Gainers & Losers")
    fig, axes = plt.subplots(1, 2, figsize=(12,5))

    axes[0].bar(gainers["Ticker"], gainers["MonthlyReturn"], color="green")
    axes[0].set_title("Top 5 Gainers")
    axes[0].set_ylabel("Monthly Return (%)")
    axes[0].tick_params(axis="x", rotation=45)

    axes[1].bar(losers["Ticker"], losers["MonthlyReturn"], color="red")
    axes[1].set_title("Top 5 Losers")
    axes[1].tick_params(axis="x", rotation=45)

    st.pyplot(fig)