import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, amount: int = 1):
        await ctx.message.delete()

        embed = discord.Embed(
            title="Robo Dick Help",
            description="Commands and aliases for Robo Dick",
            colour=discord.Colour.purple()
        )

        embed.add_field(name="Clean messages",
                        value="`clean <amount>\n\n`", inline=True)
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="\u200B", value="\u200B")

        embed.add_field(name="Stonks",
                        value="`stonk <symbol> <period> <interval>`", inline=True)
        embed.add_field(
            name="Periods", value="`1d`,`5d`,`1mo`,`3mo`,`6mo`,`1y`,`2y`,`5y`,`10y`,`ytd`,`max`")
        embed.add_field(
            name="Intervals", value="`1m`,`2m`,`5m`,`15m`,`30m`,`60m`,`90m`,`1h`,`1d`,`5d`,`1wk`,`1mo`,`3mo`")

        embed.add_field(name="Show OSRS stats",
                        value="`osrs <username>`\n\n", inline=True)
        embed.add_field(name="\u200B", value="\u200B")
        embed.add_field(name="\u200B", value="\u200B")

        embed.add_field(name="Play song",
                        value="`play <url>`\n `p`,`sing`", inline=True)
        embed.add_field(name="Pause song", value="`pause`", inline=True)
        embed.add_field(name="Resume song", value="`resume`", inline=True)
        embed.add_field(name="Skip song", value="`skip`", inline=True)
        embed.add_field(
            name="Remove song", value="`remove <position in queue>`\n `rm`,`rem`", inline=True)
        embed.add_field(name="Clear queue",
                        value="`clear`\n `clr`", inline=True)
        embed.add_field(name="Show queue",
                        value="`queue`\n `q`,`playlist`,`que`", inline=True)
        embed.add_field(
            name="Now playing", value="`playing`\n `np`,`song`,`current`,`currentsong`", inline=True)
        embed.add_field(name="Change volume",
                        value="`volume <percentage>`\n `v`,`vol`", inline=True)
        embed.add_field(name="Kick the bot off the stage",
                        value="`leave`\n `stop`,`dc`,`disconnect`,`bye`", inline=True)

        await ctx.message.author.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
