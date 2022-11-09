import discord
from discord.ext import commands
import imdb


class Movie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ia = imdb.Cinemagoer()
        self.max_tries = 5

    @commands.command()
    async def movie(self, ctx, *title):
        search = ' '.join(s for s in title)
        if search == "":
            search = "Kung fu hustle"

        base_URL = "https://www.imdb.com/title/tt"
        movies = self.ia.search_movie(search)
        tries = 0
        while len(movies) == 0:
            movies = self.ia.search_movie(search)
            tries += 1
            if tries >= self.max_tries:
                break

        if len(movies) == 0:
            await ctx.channel.send("Couldn't find movie")
        else:
            id = movies[0].movieID
            url = base_URL + id
            await ctx.channel.send(url)


async def setup(bot):
    await bot.add_cog(Movie(bot))
