from discord.ext import commands
import requests


class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        res = requests.get("https://meme-api.herokuapp.com/gimme")
        json = res.json()
        url = json["url"]
        await ctx.send(url)


async def setup(bot):
    await bot.add_cog(Meme(bot))
