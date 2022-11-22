import discord
from discord.ext import commands
import locale
import yfinance as yf
import yfinance.shared as shared
import plotly.graph_objects as go


class Stonk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        locale.setlocale(locale.LC_ALL, '')

    @commands.command()
    async def stonk(self, ctx, symbol, period="1mo", interval="1d"):
        print(symbol, period, interval)
        symbol = symbol.upper()

        if not self.ticker_exists(symbol):
            symbol = "GME"
            await ctx.channel.send("Looks like you mispelled **%s**" % symbol)

        today_data = self.todays_data(symbol)
        img = self.create_img(
            symbol, period=period, interval=interval)

        embed = discord.Embed(
            title=today_data["Name"],
            colour=discord.Colour.blue()
        )

        embed.add_field(name="Open", value=today_data["Open"], inline=True)
        embed.add_field(name="High", value=today_data["High"], inline=True)
        embed.add_field(name="Low", value=today_data["Low"], inline=True)
        embed.add_field(name="Close", value=today_data["Close"], inline=True)
        embed.add_field(name="Volume", value=today_data["Volume"], inline=True)
        embed.add_field(name="\u200B", value="\u200B")

        embed.set_author(name=symbol,
                         icon_url=today_data["Logo"])

        embed.set_image(url="attachment://stonk.png")

        await ctx.channel.send(file=img, embed=embed)

    def ticker_exists(self, symbol):
        yf.Ticker(symbol).history(period="1d")
        if(shared._ERRORS):
            shared._ERRORS = {}
            return False
        else:
            return True

    def todays_data(self, symbol):
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")

        volume = data['Volume'][0]
        volume_formatted = locale.format_string("%d", volume, grouping=True)

        return {
            "Open": "%.2f" % data["Open"][0],
            "High": "%.2f" % data["High"][0],
            "Low": "%.2f" % data["Low"][0],
            "Close": "%.2f" % data["Close"][0],
            "Volume": volume_formatted,
            "Logo": ticker.info["logo_url"],
            "Name": ticker.info["shortName"]
        }

    # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, max
    def create_img(self, symbol, period="1mo", interval="1d"):
        data = yf.download(tickers=symbol, period=period,
                           interval=interval, rounding=True, auto_adjust=True, prepost=True)
        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"], name="market data"))
        fig.update_layout(title=f"{symbol} - period: {period} - interval: {interval}",
                          yaxis_title="Stonk Price")

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

        fig.write_image("./img/stonk.png")
        return discord.File("./img/stonk.png", filename="stonk.png")


async def setup(bot):
    await bot.add_cog(Stonk(bot))
