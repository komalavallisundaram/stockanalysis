Data-Driven Stock Analysis: Organizing, Cleaning, and Visualizing Market Trends Overview 
       This project provides a Stock Performance Dashboard for the Nifty 50 index, analyzing daily stock data (open, close, high, low, volume) over the past year.
       The workflow integrates Python, Pandas, PostgreSQL, Streamlit, and Power BI to transform raw data into actionable insights.
       The dashboard highlights volatility, cumulative returns, sector performance, correlations, and monthly gainers/losers, supporting investors and analysts in making informed decisions.           

OBJECTIVES:
- Extract and clean raw stock data from YAML files.
- Store structured data in PostgreSQL for efficient querying.
- Perform statistical analysis on volatility, returns, and correlations.
- Build interactive dashboards in Streamlit and Power BI.

BUSINESS USE CASE:
- Stock Ranking: Identify top 10 gainers and losers.
- Market Overview: Summarize average performance and green vs. red stocks.
- Investment Insights: Highlight consistent growth vs. declines.
- Decision Support: Provide volatility and sector-level trends for traders.

WORKFLOW:
- Data Extraction
- Parse YAML files → Convert to CSV → Load into PostgreSQL.
- Data Cleaning
- Remove duplicates, validate schema, enrich with sector mapping.
- Analysis
- Volatility (standard deviation of daily returns).
- Cumulative returns (running total).
- Sector-wise yearly returns.
- Correlation matrix of stock returns.
- Monthly gainers/losers.
- Visualization
- Streamlit dashboard for interactive exploration.
- Power BI dashboard for professional reporting.

KEY VISUALISATION:
- Top 10 Volatile Stocks (bar chart)
- Cumulative Returns (line chart for top 5 stocks)
- Sector-wise Yearly Returns (bar chart)
- Correlation Heatmap (stock price correlations)
- Monthly Gainers & Losers (12 bar charts)

Tech stack:
    Category       | Tools |
    Languages      | Python |
|   Database       | PostgreSQL |
|   Visualization  | Streamlit, Power BI |
|   Libraries      | Pandas, Matplotlib, Seaborn, SQLAlchemy, PyYAML |

Deliverables
- SQL Database: Clean and processed stock data
- Python Scripts: Extraction, cleaning, analysis, DB interaction
- Power BI Dashboard: Sector and performance insights
- Streamlit App: Interactive dashboard for real-time analysis

1. Clone the Repository
https://github.com/komalavallisundaram/stockanalysis

2. Install Dependencies
pip install -r requirements.txt

3. Prepare Data
- Place YAML files in the data/ folder.
- Run extraction scripts to generate master_csv.csv.
4. Run Analysis Scripts
python extract_master.py
python analysis.py
python dashboard.py

5. Launch Streamlit Dashboard
streamlit run dashboard.py

6. Power BI Dashboard
- Import processed CSV/SQL tables into Power BI.
- Build visuals using provided metrics.

Example Visuals
- Cumulative Return by Ticker
- Yearly Return by Sector
- Volatility by Ticker
- Monthly Return by Ticker and YearMonth
- Correlation Heatmap

PROJECT STRUCTURE:
stock-analysis-dashboard/
├── data/                     
├── scripts/                  
│   ├── extract_master.py
│   ├── analysis.py
│   
│   
├── dashboard.py              # Streamlit app
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── powerbi                   # Power BI dashboard files