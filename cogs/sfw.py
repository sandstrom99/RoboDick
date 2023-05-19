import os
import random
import nextcord
from nextcord.ext import commands
import requests
import uuid
import utils.image

IMG_PATH = "./img/sfw/"
SFW_CHANNEL_NAME = "sfw-img-requests"


class Sfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.datasource = utils.image.ImageDatasource(IMG_PATH)

    @commands.command()
    async def sfw(self, ctx, count=1):
        if count > 9:
            return await ctx.channel.send(content="Too many pictures man. Max is 9")

        files: list[nextcord.File]= []
        for i in range(count):
            random_image = self.datasource.get_random_path()
            file = nextcord.File(random_image)
            files.append(file)
        return await ctx.channel.send(files=files)

    @commands.command()
    async def sfwcount(self, ctx):
        count = self.datasource.count()
        return await ctx.channel.send(content="SFW Image Count: %d" % count)

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


def setup(bot):
    bot.add_cog(Sfw(bot))
