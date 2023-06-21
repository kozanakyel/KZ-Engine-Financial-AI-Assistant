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
    data_with_supertrend = pd.concat([data, sti], axis=1)

    return data_with_supertrend

def create_ichmiouk_kijunsen(dft: pd.DataFrame()) -> None:
    period26_high = dft['High'].rolling(window=26).max()
    period26_low = dft['Low'].rolling(window=26).min()
    dft['ich_kline'] = (period26_high + period26_low) / 2

def create_ichmiouk_tenkansen(dft: pd.DataFrame()) -> None:
    period26_high = dft['High'].rolling(window=9).max()
    period26_low = dft['Low'].rolling(window=9).min()
    dft['ich_tline'] = (period26_high + period26_low) / 2
    
def analyze_ichimoku(dft, n=10):
    # Get the last `n` rows of the DataFrame
    last_rows = dft.iloc[-n:]

    # Initialize a variable to store the trend
    trend = "undefined"

    for i in range(1, len(last_rows)):
        # Check for Conversion Line crossing above Base Line
        if last_rows.iloc[i-1]['ich_tline'] < last_rows.iloc[i-1]['ich_kline'] and last_rows.iloc[i]['ich_tline'] > last_rows.iloc[i]['ich_kline']:
            trend = "bullish"
        # Check for Conversion Line crossing below Base Line
        elif last_rows.iloc[i-1]['ich_tline'] > last_rows.iloc[i-1]['ich_kline'] and last_rows.iloc[i]['ich_tline'] < last_rows.iloc[i]['ich_kline']:
            trend = "bearish"

    # Check if the Close price is above the Conversion Line and Base Line
    if last_rows.iloc[-1]['Close'] > last_rows.iloc[-1]['ich_tline'] and last_rows.iloc[-1]['Close'] > last_rows.iloc[-1]['ich_kline']:
        trend = "strong bullish"
    # Check if the Close price is below the Conversion Line and Base Line
    elif last_rows.iloc[-1]['Close'] < last_rows.iloc[-1]['ich_tline'] and last_rows.iloc[-1]['Close'] < last_rows.iloc[-1]['ich_kline']:
        trend = "strong bearish"

    return trend

def analyze_supertrend(data):
    # Get the last 10 rows of the DataFrame
    last_rows = data.iloc[-5:]

    # Define initial values
    trend = "undefined"
    price_crossed_line = False

    # Check each pair of rows in the last 10 rows
    for i in range(1, len(last_rows)):
        if last_rows.iloc[i]['SUPERTd_7_3.0'] == 1:
            trend = "uptrend"
            if last_rows.iloc[i-1]['Close'] < last_rows.iloc[i-1]['SUPERT_7_3.0'] and last_rows.iloc[i]['Close'] > last_rows.iloc[i]['SUPERT_7_3.0']:
                price_crossed_line = True

        elif last_rows.iloc[i]['SUPERTd_7_3.0'] == -1:
            trend = "downtrend"
            if last_rows.iloc[i-1]['Close'] > last_rows.iloc[i-1]['SUPERT_7_3.0'] and last_rows.iloc[i]['Close'] < last_rows.iloc[i]['SUPERT_7_3.0']:
                price_crossed_line = True

    return trend, price_crossed_line

if __name__ == '__main__':
    df = fetch_data('BTC-USD', '3mo', '1d')
    indicator_data = calculate_dmi_rsi_mfi(df)
    result_ich = analyze_ichimoku(indicator_data)
    print(indicator_data.info())
    print(f'Ichmouku analyze and trend directions: {result_ich}')
    sti = calculate_supertrend(indicator_data)
    trend, price_crossed_line = analyze_supertrend(sti)
    print(f"The current trend is {trend}. Did the price cross the SuperTrend line in the last 10 periods? {'Yes' if price_crossed_line else 'No'}")
