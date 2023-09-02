import logging

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import yfinance as yf
from bs4 import BeautifulSoup


def extract_transform_ticker(url: str) -> list[str]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Define tag and class that contain the ticker name
    tag_ticker = soup.findAll(
        "a",
        {"class": "apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat"},
    )
    # Note: maybe the class name have changed.
    try:
        if not tag_ticker:
            raise ValueError("'tag_ticker' is empty.")

    except ValueError as e:
        logging.error(e)

    ticker_list = []
    [ticker_list.append(ticker.text) for ticker in tag_ticker]

    ticker_cleaning = [ticker + ".BK" for ticker in ticker_list]
    return ticker_cleaning


def transform_ohlc_df(
    ticker_list: list[str], start_date: str, end_date: str
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    open_df, high_df, low_df, close_df, adj_df, volume = (
        pd.DataFrame() for _ in range(6)
    )

    # Loop through the stock symbols and retrieve data for each
    for symbol in ticker_list:
        # Pull data for the current stock symbol
        data = yf.download(symbol, start=start_date, end=end_date)

        # Format column and index as lower case
        data = data.rename(columns={"Adj Close": "adj_close"})
        data.columns = data.columns.str.lower()
        data.index.name = data.index.name.lower()

        # Add the OHLC as a column in the DataFrame
        # open_df[symbol] = data['open']
        # high_df[symbol] = data['high']
        # low_df[symbol] = data["low"]
        close_df[symbol] = data["close"]
        # adj_df[symbol] = data['adj_close']
        # volume[symbol] = data['volume']

    return open_df, high_df, low_df, close_df, adj_df


def bar_plot(close_df: pd.DataFrame, ma_df: pd.DataFrame, title="Bar Plot of Data"):
    # Data preprocessing
    data = pd.DataFrame(data=(close_df > ma_df).sum(axis=1))

    # Create a bar plot using Plotly Express
    fig = px.bar(
        data_frame=data,
        x=data.index,  # Note: fixed plot the weekend.
        y=data.iloc[:, -1],
        title=title,
        color_discrete_sequence=["skyblue"],
    )

    # Zoom in the last 20 bars. (represent 1 month)
    start_scope_date = data.index[-20].strftime("%Y-%m-%d")
    end_scope_date = data.index[-1].strftime("%Y-%m-%d")

    # Customize the layout
    fig.update_layout(
        xaxis=dict(
            range=[start_scope_date, end_scope_date]  # Set the x-axis range here
        ),
        xaxis_title=None,
        yaxis_title=None,
    )

    # Show the plot
    st.plotly_chart(fig)
