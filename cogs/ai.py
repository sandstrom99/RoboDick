import discord
from discord.ext import commands
import aiohttp
import time
from io import BytesIO
import base64
import cv2 as cv
import numpy as np

number_emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(
    num) for num in range(1, 10)]


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def img_to_np(self, img):
        return cv.imdecode(np.frombuffer(base64.decodebytes(img.encode("utf-8")), np.uint8), -1)

    def images_to_grid(self, images):
        return np.vstack([
            np.hstack([
                self.img_to_np(images[0]),
                self.img_to_np(images[1]),
                self.img_to_np(images[2]),
            ]),
            np.hstack([
                self.img_to_np(images[3]),
                self.img_to_np(images[4]),
                self.img_to_np(images[5]),
            ]),
            np.hstack([
                self.img_to_np(images[6]),
                self.img_to_np(images[7]),
                self.img_to_np(images[8]),
            ])
        ])

    @commands.command()
    async def ai(self, ctx, *, prompt: str):
        self.prompt = prompt
        ETA = int(time.time() + 60)
        ETA_msg = await ctx.send(f"Generating images - ETA: <t:{ETA}:R>")
        async with aiohttp.request("POST", "https://backend.craiyon.com/generate", json={"prompt": prompt}) as resp:
            data = await resp.json()
            self.images = data["images"]

            img_grid = self.images_to_grid(self.images)
            img_grid = cv.resize(img_grid, dsize=(
                1500, 1500), interpolation=cv.INTER_NEAREST)
            cv.imwrite("./img/ai_grid.png", img_grid)
            await ETA_msg.delete()
            img_msg = await ctx.send(content=f"Generated images of '{prompt}'", file=discord.File("./img/ai_grid.png", "generated_images.png"))
            for emoji in number_emojis:
                await img_msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and self.prompt in reaction.message.content:
            index = number_emojis.index(reaction.emoji)
            img = self.images[index]
            img = self.img_to_np(img)
            cv.imwrite("./img/ai_img.png", img)
            await reaction.message.channel.send(content=f"AI Image {index+1}", file=discord.File("./img/ai_img.png", "generated_image.png"))


async def setup(bot):
    await bot.add_cog(AI(bot))
