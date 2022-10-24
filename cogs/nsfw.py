from discord.ext import commands
import requests


class Nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nsfw(self, ctx):
        res = requests.get("https://scathach.redsplit.org/v3/nsfw/gif")
        json = res.json()
        url = json["url"]
        await ctx.send(url)


async def setup(bot):
    await bot.add_cog(Nsfw(bot))
