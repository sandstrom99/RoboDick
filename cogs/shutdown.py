import discord
from discord.ext import commands
import sys

SHUTDOWN_PASSWORD = "Yeet1337"


class Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def shutdown(self, ctx, password=""):
        if password == SHUTDOWN_PASSWORD:
            await ctx.message.delete()
            sys.exit()
        else:
            await ctx.message.add_reaction("\U0001F621")
            await ctx.message.add_reaction("\U0001F624")
            await ctx.message.add_reaction("\U0001F620")
            await ctx.message.add_reaction("\U00002620")
            await ctx.message.add_reaction("\U0001F92C")
            await ctx.message.add_reaction("\U0001F480")
            await ctx.message.add_reaction("\U0001F595")
            await ctx.channel.send("Don't fucking shut me down you piece of shit")


async def setup(bot):
    await bot.add_cog(Shutdown(bot))
