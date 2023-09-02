from datetime import datetime

import pandas_ta as ta
import streamlit as st

from src.utils import bar_plot, extract_transform_ticker, transform_ohlc_df

st.set_page_config(
    page_title="Thai Market Dashboard", page_icon=":bar_chart:", layout="centered"
)
st.title("Thai Market Dashboard")

# get ticker name in list SET50
ticker_cleaning = extract_transform_ticker(
    url="https://www.tradingview.com/symbols/SET-SET50/components/"
)

start_date = "2022-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")

ticker_cleaning = ticker_cleaning[0:10]  # mock

st.subheader("Ticker")
ticker_names = ",".join(ticker_cleaning)

_, _, _, close_df, _ = transform_ohlc_df(
    ticker_list=ticker_cleaning, start_date=start_date, end_date=end_date
)

ma20_df = close_df.apply(lambda x: ta.ema(x, 20))
ma50_df = close_df.apply(lambda x: ta.ema(x, 50))
ma100_df = close_df.apply(lambda x: ta.ema(x, 100))

st.subheader("Momentum Price")
bar_plot(close_df=close_df, ma_df=ma20_df, title="Amount ticker over EMA20")
bar_plot(close_df=close_df, ma_df=ma20_df, title="Amount ticker over EMA50")
bar_plot(close_df=close_df, ma_df=ma20_df, title="Amount ticker over EMA100")
