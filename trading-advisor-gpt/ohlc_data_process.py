import yfinance as yf
import pandas as pd
import pandas_ta as ta


def fetch_data(symbol: str, period: str, interval: str):
    # Fetch Bitcoin data from Yahoo Finance
    ohlc_data = yf.download(tickers=symbol, period=period, interval=interval, progress=False)
    return ohlc_data


def calculate_dmi_rsi_mfi(data):
    data.ta.adx(length=14, append=True)
    data.ta.rsi(length=14, append=True)
    data.ta.mfi(length=14, append=True)
    data = data.dropna(axis=0)
    return data


if __name__ == '__main__':
    df = fetch_data('BTC-USD', '3mo', '1d')
    indicator_data = calculate_dmi_rsi_mfi(df)
    print(indicator_data.info())
