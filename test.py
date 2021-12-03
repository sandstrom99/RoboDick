import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import yfinance as yf

symbol = "GME"

period = "1mo"
interval = "1h"

data = yf.download(tickers=symbol, period=period,
                   interval=interval, prepost=True)

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"], name="market data"))
fig.update_layout(title=symbol + " Stonk price",
                  yaxis_title="Stock Price (USD)")
fig.update_xaxes(rangeslider_visible=False)

if '-' not in symbol:
    if 'h' in interval:
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),
                dict(bounds=[17, 9], pattern="hour")
            ]
        )
    else:
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),
            ]
        )

fig.write_image("./stonk.png")
