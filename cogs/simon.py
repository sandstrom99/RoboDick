import nextcord
from nextcord.ext import commands
import os
import random
import utils.image

IMG_PATH = "./img/simon/"

class Simon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.datasource = utils.image.ImageDatasource(IMG_PATH)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "simon":
            random_image = self.datasource.get_random_path()

            file = nextcord.File(random_image)
            text = "Here's a picture of Simon"
            return await message.channel.send(text, file=file)

        if "simon" in message.content.lower():
            return await message.add_reaction("\U0001F60D")


def setup(bot):
    bot.add_cog(Simon(bot))
