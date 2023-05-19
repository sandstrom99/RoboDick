from nextcord.ext import commands
import requests


class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ball8(self, ctx, *, search: str):
        res = requests.get(f"https://8ball.delegator.com/magic/JSON/{search}")
        json = res.json()
        print(json)
        answer = json["magic"]["answer"]
        await ctx.send(answer)


def setup(bot):
    bot.add_cog(EightBall(bot))
