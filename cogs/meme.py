import nextcord
from nextcord.ext import commands
import requests

class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        res = requests.get("https://meme-api.com/gimme")
        json = res.json()

        url = json["url"]
        title = json["title"]
        poster = json["author"]
        subreddit = json["subreddit"]
        link = json["postLink"]

        embed = nextcord.Embed(title=title, color=nextcord.Colour.blue())
        embed.set_image(url=url)
        embed.add_field(name="Subreddit", value=subreddit)
        embed.add_field(name="Poster", value=poster)
        embed.add_field(name="Post link", value=link)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Meme(bot))
