from nextcord.ext import commands
from random import randint


class Rand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rand(self, ctx, n1=None, n2=None):
        if n1 is None and n2 is None:
            n1 = 1
            n2 = 100
        elif n2 is None:
            n2 = int(n1)
            n1 = 1
        else:
            n1 = int(n1)
            n2 = int(n2)

        x = randint(n1, n2)
        await ctx.channel.send(f"Random number between {n1} and {n2}: {x}")


def setup(bot):
    bot.add_cog(Rand(bot))
