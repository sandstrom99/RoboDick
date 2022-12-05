import os
import random
import discord
from discord.ext import commands
import requests
import uuid

IMG_PATH = "./img/sfw/"
SFW_CHANNEL_NAME = "sfw-img-requests"


class Sfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sfw(self, ctx):
        files = os.listdir(IMG_PATH)
        random_image = random.choice(files)

        file = discord.File(IMG_PATH + random_image)
        return await ctx.channel.send(file=file)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel_name = message.channel.name
        if channel_name == SFW_CHANNEL_NAME and len(message.attachments) > 0 and message.author != self.bot.user:
            for attachment in message.attachments:
                url = attachment.url
                img_name = attachment.filename
                img_extention = img_name.split(".")[1]
                if img_extention in ["jpg", "jpeg", "png"]:
                    img_data = requests.get(url).content
                    img_path = f"{IMG_PATH}{uuid.uuid1().hex}.{img_extention}"
                    with open(img_path, "wb") as handler:
                        handler.write(img_data)

            await message.add_reaction("\U0001F44C")


async def setup(bot):
    await bot.add_cog(Sfw(bot))
