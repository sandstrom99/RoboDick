import discord
from discord.ext import commands
from osrs_api.const import SKILLS
from osrs_api import Hiscores
import locale


class OSRS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        locale.setlocale(locale.LC_ALL, '')

    @commands.command()
    async def osrs(self, ctx, username: str):
        user = Hiscores(username)
        embed = discord.Embed(
            title="OSRS Stats: " + username,
            colour=discord.Colour.green()
        )

        total_xp = locale.format_string("%d", user.total_xp, grouping=True)
        total_level = user.total_level
        rank = user.rank

        embed.add_field(name="Total level", value=total_level)
        embed.add_field(name="Total XP", value=total_xp)
        embed.add_field(name="Rank", value=rank)

        for _ in range(3):
            embed.add_field(name="\u200B", value="\u200B")

        for skill in SKILLS:
            name = skill[0].upper() + skill[1:]
            embed.add_field(name=name, value=user.skills[skill].level)

        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(OSRS(bot))
