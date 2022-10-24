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

        total_xp = locale.format_string("%d", user.total_xp, grouping=True)
        total_level = user.total_level
        rank = user.rank

        embed = discord.Embed(
            title="OSRS Stats: " + username,
            description="Total XP: " +
            str(total_xp) + ", Rank: " + str(total_level),
            colour=discord.Colour.green()
        )

        embed.add_field(name="Attack",       value=user.skills["attack"].level)
        embed.add_field(name="Hitpoints",
                        value=user.skills["hitpoints"].level)
        embed.add_field(name="Mining",       value=user.skills["mining"].level)
        embed.add_field(name="Strength",
                        value=user.skills["strength"].level)
        embed.add_field(name="Agility",
                        value=user.skills["agility"].level)
        embed.add_field(name="Smithing",
                        value=user.skills["smithing"].level)
        embed.add_field(name="Defence",
                        value=user.skills["defence"].level)
        embed.add_field(name="Herblore",
                        value=user.skills["herblore"].level)
        embed.add_field(name="Fishing",
                        value=user.skills["fishing"].level)
        embed.add_field(name="Ranged",       value=user.skills["ranged"].level)
        embed.add_field(name="Thieving",
                        value=user.skills["thieving"].level)
        embed.add_field(name="Cooking",
                        value=user.skills["cooking"].level)
        embed.add_field(name="Prayer",       value=user.skills["prayer"].level)
        embed.add_field(name="Crafting",
                        value=user.skills["crafting"].level)
        embed.add_field(name="Firemaking",
                        value=user.skills["firemaking"].level)
        embed.add_field(name="Magic",        value=user.skills["magic"].level)
        embed.add_field(name="Fletching",
                        value=user.skills["fletching"].level)
        embed.add_field(name="Woodcutting",
                        value=user.skills["woodcutting"].level)
        embed.add_field(name="Runecrafting",
                        value=user.skills["runecrafting"].level)
        embed.add_field(name="Slayer",       value=user.skills["slayer"].level)
        embed.add_field(name="Farming",
                        value=user.skills["farming"].level)
        embed.add_field(name="Construction",
                        value=user.skills["construction"].level)
        embed.add_field(name="Hunter",       value=user.skills["hunter"].level)
        embed.add_field(name="Total level",  value=total_level)

        await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(OSRS(bot))
