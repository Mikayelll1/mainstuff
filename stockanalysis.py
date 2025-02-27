import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import ta

# Fetch stock data based on the ticker, period and interval
def fetch_stock_data(ticker, period, interval):
    end_date = datetime.now()
    if period == "1wk":
        start_date = end_date - timedelta(days=7)
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)
    return data

# Process data to ensure it is timezone-aware and has the correct format
def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data

# Calculate basic metrics from the stock data
def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, change, pct_change, high, low, volume

# Add simple moving average (SMA) and exponential moving average (EMA) indicators
def add_technical_indicators(data):
    data['SMA_20'] = pd.Series(ta.trend.sma_indicator(data['Close'], window=20), index=data.index)
    data['EMA_20'] = pd.Series(ta.trend.ema_indicator(data['Close'], window=20), index=data.index)

    return data



# Set up Streamlit Page Layout
st.set_page_config(layout="wide")
st.title("Real Time Stock Dashboard")


# Sidebar for user input parameters
st.sidebar.header("Chart Parameters")
ticker = st.sidebar.text_input("Ticker", "AAPL")
time_period = st.sidebar.selectbox("Time Period", ["1d", "1wk", "1mo", "1y", "max"])
chart_type = st.sidebar.selectbox("Chart Type", ["Candlestick", "Line"])
indicators = st.sidebar.multiselect("Indicators", ["SMA 20", "EMA 20"])

# Mapping of time periods to data intervals
interval_mapping = {
    "1d": "1m",
    "1wk": "30m",
    "1mo": "1d",
    "1y": "1wk",
    "max": "1wk"
}




# Main functions called as data variable
data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
data = process_data(data)
data = add_technical_indicators(data)

last_close, change, pct_change, high, low, volume = calculate_metrics(data)

# Display main metrics
st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")

col1, col2, col3 = st.columns(3)
col1.metric(label="High", value=f"{high:.2f} USD")
col2.metric(label="Low", value=f"{low:.2f} USD")
col3.metric(label="Volume", value=f"{volume:.0f}")

fig = go.Figure()
if chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(x=data['Datetime'],
                                    open=data['Open'],
                                    high=data['High'],
                                    low=data['Low'],
                                    close=data['Close'],
                                    name="Candlestick"))
else:
    fig = px.line(data, x="Datetime", y="Close")

# Add selected technical indicators to the chart
for indicator in indicators:
    if indicator == "SMA 20":
        fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], mode='lines', name='SMA 20'))
    elif indicator == "EMA 20":
        fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], mode='lines', name='EMA 20'))

    # Format graph
fig.update_layout(title=f"{ticker} Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    height=600)
st.plotly_chart(fig, use_container_width=True)

# Display historical data and technical indicators
st.subheader("Historical Data")
st.dataframe(data[["Datetime", "Open", "High", "Low", "Close", "Volume"]])

st.subheader("Technical Indicators")
st.dataframe(data[["Datetime", "SMA_20", "EMA_20"]])


# Sidebar section for real-time stock prices of selected symbols
st.sidebar.header("Real-Time Stock Prices")
stock_symbols = ["AAPL", "GOOGL", "AMZN", "MSFT"]
for symbol in stock_symbols:
    real_time_data = fetch_stock_data(symbol, "1d", "1m")
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = real_time_data["Close"].iloc[-1]
        change = last_price - real_time_data["Open"].iloc[0]
        pct_change = (change / real_time_data["Open"].iloc[0]) * 100
        print(type(last_price))
        st.sidebar.metric(f"{symbol}", f"{last_price:.2f} USD", f"({change:.2f}, {pct_change:.2f}%)")

# Sidebar information section
st.sidebar.subheader("About")
st.sidebar.info("Im working on a donation button soon, please give whatever you can to a homeless programmer")