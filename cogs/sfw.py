import os
import random
import discord
from discord.ext import commands

IMG_PATH = "./img/sfw/"


class Sfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sfw(self, ctx):
        files = os.listdir(IMG_PATH)
        random_image = random.choice(files)

        file = discord.File(IMG_PATH + random_image)
        return await ctx.channel.send(file=file)


async def setup(bot):
    await bot.add_cog(Sfw(bot))
