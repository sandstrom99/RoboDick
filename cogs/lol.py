import discord
from discord.ext import commands
import requests

TOKEN = "RGAPI-0a5684b9-b049-4c64-96fe-a34e1b00e799"


class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_profile(self, region, name):
        if region == "eune":
            API_Riot = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
                name + "?api_key=" + TOKEN
        elif region == "euw":
            API_Riot = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + \
                name + "?api_key=" + TOKEN
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
                id + "?api_key=" + TOKEN
        elif region == "euw":
            API_Riot = "https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + \
                id + "?api_key=" + TOKEN
        else:
            API_Riot = ""
        response = requests.get(API_Riot)
        summonerJson = response.json()
        calls = {0: "queueType", 1: "tier", 2: "rank",
                 3: "leaguePoints", 4: "wins", 5: "losses"}
        ranks = []
        try:
            for i in range(3):
                for j in range(6):
                    ranks.append(summonerJson[i][calls[j]])
        except:
            pass
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

            # flex
            try:
                tmp = f"{ranks[1]} {ranks[2]} · LP:{ranks[3]} · Wins: {ranks[4]} · Losses: {ranks[5]}"
                embed.add_field(name=ranks[0], value=tmp, inline=False)
            except:
                embed.add_field(name="Not found",
                                value="Player hasn't any ranked status")

            # solo duo
            try:
                tmp = f"{ranks[7]} {ranks[8]} · LP:{ranks[9]} · Wins: {ranks[10]} · Losses: {ranks[11]}"
                embed.add_field(name=ranks[6], value=tmp, inline=False)
            except:
                embed.add_field(name="Not found",
                                value="Player hasn't any ranked status")

            # tft
            try:
                tmp = f"{ranks[13]} {ranks[14]} · LP:{ranks[15]} · Wins: {ranks[16]} · Losses: {ranks[17]}"
                embed.add_field(name=ranks[12], value=tmp, inline=False)
            except:
                embed.add_field(name="Not found",
                                value="Player hasn't any ranked status")

            await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Lol(bot))
