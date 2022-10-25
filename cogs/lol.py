import discord
from os import getenv
from discord.ext import commands
import requests


class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = getenv("RIOT_API_TOKEN")

    def get_profile(self, region, name):
        if region == "eune":
            API_Riot = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
                name + "?api_key=" + self.token
        elif region == "euw":
            API_Riot = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
                name + "?api_key=" + self.token
        else:
            return None

        response = requests.get(API_Riot)
        summonerJson = response.json()
        if "status" in summonerJson:
            return None
        else:
            s_name = summonerJson["name"]
            s_level = "Lvl. " + str(summonerJson["summonerLevel"])
            s_icon = "http://ddragon.leagueoflegends.com/cdn/12.13.1/img/profileicon/" + \
                str(summonerJson["profileIconId"]) + ".png"
            s_id = summonerJson["id"]
            return (s_name, s_level, s_icon, s_id)

    def fetchRanks(self, region, id):
        if region == "eune":
            API_Riot = "https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + \
                id + "?api_key=" + self.token
        elif region == "euw":
            API_Riot = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + \
                id + "?api_key=" + self.token
        else:
            API_Riot = ""
        response = requests.get(API_Riot)
        summonerJson = response.json()
        ranks = {}

        for r in summonerJson:
            qt = r["queueType"]
            ranks[qt] = r
        return ranks

    @commands.command()
    async def lol(self, ctx, *name_with_spaces):
        name = ' '.join(s for s in name_with_spaces)
        region = "euw"
        summoner = self.get_profile(region, name)
        if summoner is None:
            await ctx.channel.send("Invalid EUW LoL name")
        else:
            ranks = self.fetchRanks(region, summoner[3])

            embed = discord.Embed(
                title=summoner[0], description=summoner[1], color=0xFFD500)
            embed.set_thumbnail(url=summoner[2])

            # solo duo
            if "RANKED_SOLO_5x5" in ranks:
                rank = ranks["RANKED_SOLO_5x5"]
                tmp = '%s %s · LP: %d · Wins: %d · Losses: %d' % (
                    rank["tier"], rank["rank"], rank["leaguePoints"], rank["wins"], rank["losses"])
                embed.add_field(name="Ranked Solo/Duo",
                                value=tmp, inline=False)
            else:
                embed.add_field(name="Ranked Solo/Duo",
                                value="Player has no ranked status")

            # flex
            if "RANKED_FLEX_SR" in ranks:
                rank = ranks["RANKED_FLEX_SR"]
                tmp = '%s %s · LP: %d · Wins: %d · Losses: %d' % (
                    rank["tier"], rank["rank"], rank["leaguePoints"], rank["wins"], rank["losses"])
                embed.add_field(name="Ranked Flex", value=tmp, inline=False)
            else:
                embed.add_field(name="Ranked Flex",
                                value="Player has no ranked status")

            # TFT
            if "RANKED_TFT_DOUBLE_UP" in ranks:
                rank = ranks["RANKED_TFT_DOUBLE_UP"]
                tmp = '%s %s · LP: %d · Wins: %d · Losses: %d' % (
                    rank["tier"], rank["rank"], rank["leaguePoints"], rank["wins"], rank["losses"])
                embed.add_field(name="Ranked TFT", value=tmp, inline=False)
            else:
                embed.add_field(name="Ranked TFT",
                                value="Player has no ranked status")
            await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Lol(bot))
