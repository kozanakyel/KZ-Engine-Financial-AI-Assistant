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
    create_ichmiouk_kijunsen(data)
    create_ichmiouk_tenkansen(data)
    data = data.dropna(axis=0)
    return data

def calculate_supertrend(data):
    """
    SUPERT_7_3.0: This is the actual SuperTrend line. It follows the price and flips its position when the price crosses it.
    SUPERTd_7_3.0: This is the SuperTrend direction. It gives +1 for an uptrend and -1 for a downtrend.
    SUPERTl_7_3.0: This represents the lower band of the SuperTrend indicator during an uptrend. It is NaN during a downtrend.
    SUPERTs_7_3.0: This represents the upper band of the SuperTrend indicator during a downtrend. It is NaN during an uptrend.
    """
    sti = ta.supertrend(data['High'], data['Low'], data['Close'], length=7, multiplier=3)

    return sti

def create_ichmiouk_kijunsen(dft: pd.DataFrame()) -> None:
    period26_high = dft['High'].rolling(window=26).max()
    period26_low = dft['Low'].rolling(window=26).min()
    dft['ich_kline'] = (period26_high + period26_low) / 2

def create_ichmiouk_tenkansen(dft: pd.DataFrame()) -> None:
    period26_high = dft['High'].rolling(window=9).max()
    period26_low = dft['Low'].rolling(window=9).min()
    dft['ich_tline'] = (period26_high + period26_low) / 2


if __name__ == '__main__':
    df = fetch_data('BTC-USD', '3mo', '1d')
    indicator_data = calculate_dmi_rsi_mfi(df)
    print(indicator_data.info())
