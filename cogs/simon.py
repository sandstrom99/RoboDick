import discord
from discord.ext import commands
import glob
import os
import random

IMG_PATH = "./img/simon/"


class Simon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "simon":
            files = os.listdir(IMG_PATH)
            random_image = random.choice(files)

            file = discord.File(IMG_PATH + random_image)
            text = "Here's a picture of Simon"
            return await message.channel.send(text, file=file)

        if "simon" in message.content.lower():
            return await message.add_reaction("\U0001F60D")


async def setup(bot):
    await bot.add_cog(Simon(bot))
