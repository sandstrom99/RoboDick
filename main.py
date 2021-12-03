import os
import random
import discord
from discord.ext import commands

TOKEN = "OTE0OTczMjI3MzMwMTc5MDgy.YaU1OA.hDf2DPLj3ARtd9852e7tfwpIoT0"

PREFIX = '.'

bot = commands.Bot(command_prefix=PREFIX)

bot.remove_command("help")


@bot.event
async def on_ready():
    print("Bot is running")
    await bot.change_presence(activity=discord.Game(name=".help"))
    with open("./img/avatar.png", "rb") as fp:
        img = fp.read()
        await bot.user.edit(avatar=img)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith(PREFIX):
        await bot.process_commands(message)

if __name__ == "__main__":
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e:
                print(e)
                pass

    bot.run(TOKEN)
