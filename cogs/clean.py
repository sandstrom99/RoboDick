from nextcord.ext import commands


class Clean(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clean(self, ctx, amount: int = 1):
        amount = min(20, amount)
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)


def setup(bot):
    bot.add_cog(Clean(bot))
