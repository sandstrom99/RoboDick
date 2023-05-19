import nextcord
from nextcord.ext import commands
import openai
import os
import random
from os import getenv

class GTP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = getenv("OPENAI_API_TOKEN")
        self.model = "gpt-3.5-turbo"

    @commands.command()
    async def gpt(self, ctx, *, prompt: str):
        chat_completion = openai.ChatCompletion.create(model=self.model, messages=[{"role": "user", "content": prompt}])
        response = chat_completion.choices[0].message.content
        print(response)
        await ctx.message.channel.send(content=response)


def setup(bot):
    bot.add_cog(GTP(bot))
