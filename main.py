import asyncio
import os
from os import getenv
from dotenv import load_dotenv
import random
import discord
from discord.ext import commands

PREFIX = '.'


class RoboDick:
    def __init__(self):
        self.token = getenv("DISCORD_BOT_TOKEN")

        self.bot = commands.Bot(command_prefix=PREFIX,
                                intents=discord.Intents.all())
        self.bot.remove_command("help")
        self.add_events()

    async def init_cogs(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await self.bot.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    print(e)
                    pass

    def add_events(self):
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)

    async def on_ready(self):
        print("Bot is running")
        await self.init_cogs()

        await self.bot.change_presence(activity=discord.Game(name=".help"))
        with open("./img/avatar.png", "rb") as fp:
            img = fp.read()
            await self.bot.user.edit(avatar=img)

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith(PREFIX):
            await self.bot.process_commands(message)

    def start_bot(self):
        self.bot.run(self.token)


if __name__ == "__main__":
    load_dotenv(".env")
    b = RoboDick()

    print("Starting RoboDick")
    b.start_bot()
