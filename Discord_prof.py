import json
import random

import discord
from discord.ext import commands

import operator

import Settings

Settings.init()
IDsDic = Settings.IDsDic
regEmoj = Settings.RegEmojDic

# Json paths.
profJsonPath = "Jsons_Profiles"
dailyLovePath = "Jsons_Profiles/Daily_Love.json"
lovePath = "Jsons_Profiles/Loves.json"
dailyChipsPath = "Jsons_Profiles/Daily_Chips.json"
chipsPath = "Jsons_Profiles/Chips.json"

# Open files.
# TODO: Check if jsons are empty and if yes add the {} so they wont break.
with open(dailyLovePath) as f:
    LoveAllowance = json.load(f)
with open(lovePath) as f:
    LovesDic = json.load(f)
with open(dailyChipsPath) as f:
    ChipAllowance = json.load(f)
with open(chipsPath) as f:
    ChipsDic = json.load(f)


def Commands():
    commList = ["love",
                "dailychips",
                "givechips",
                "profile",
                "loveldr",
                "chipldr"]
    commsExplanation = ["Give a love to someone.",
                        "Get your daily chips.",
                        "Give chips to someone.",
                        "Check out your profile information.",
                        "See who has the most love.",
                        "See who has the most chips."]

    return commList, commsExplanation


def JsonUpdate(jsonName, dicName):
    with open(jsonName, 'w') as file:
        for key in dicName:
            dicName.update({key: 0})
        file.write(json.dumps(dicName, sort_keys=True, indent=4, separators=(',', ': ')))


async def IsARGValid(ctx, arg, commandName):
    # Check if argument is a valid person, not a role or invalid.
    if arg is None:
        await ctx.send(embed=Settings.OnErrorMessage(commandName, 0))
        return False
    try:
        user = await Settings.ChangeArgToUser(ctx, arg)
    except:
        await ctx.send(embed=Settings.OnErrorMessage(commandName, 1))
        return False

    # Check if the author tagged a bot or themselves.
    if user == ctx.author or user.bot:
        await ctx.send(embed=Settings.OnErrorMessage(commandName, 2))
        return False
    return True


def GetLdr(path, title):
    # Open the json.
    with open(path) as file:
        jsonDic = json.load(file)

    # Sort the dictionary
    listJson = sorted(jsonDic.items(), key=operator.itemgetter(1), reverse=True)
    sortedDict = dict(listJson)

    # Set the description.
    desc = ""
    i = 0
    for key in sortedDict:
        if i == 5:
            break
        desc += key + " " + str(sortedDict[key]) + "\n"
        i += 1
    # Make the embed.
    ldrEmbed = discord.Embed(title=title,
                             description=desc,
                             color=Settings.generalColorEMB)

    return ldrEmbed


def GetJsonData(dic, name):
    ret = name + ":\n"
    for key in dic:
        ret += '"' + str(key).replace("@", "") + '":' + str(dic[key]) + ",\n"
    return ret


class Discord_prof(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def love(self, ctx, arg=None):
        if not await IsARGValid(ctx, arg, "love"):
            return

        # Change the arg.
        user = await Settings.ChangeArgToUser(ctx, arg)

        # Change the author id.
        author = Settings.ChangeAuthorID(ctx)

        # Add the author to the allowance json.
        Settings.CheckNameInJson(author, profJsonPath, LoveAllowance, "Daily_Love", 0)

        if LoveAllowance[author] == 0:  # Check if author is allowed to give love.
            with open(dailyLovePath, 'w') as file:
                LoveAllowance[author] = 1
                file.write(json.dumps(LoveAllowance, sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            # Return an error message that the author already gave a love today.
            await ctx.send(embed=Settings.OnErrorMessage('love', 3))
            return

        # Replace the ! to the user mentioned.
        userMentioned = user.mention.replace('!', '')

        # Add the user mentioned to the loves json.
        Settings.CheckNameInJson(userMentioned, profJsonPath, LovesDic, "Loves", 0)
        with open(lovePath, 'w') as file:
            LovesDic[userMentioned] += 1
            file.write(json.dumps(LovesDic, sort_keys=True, indent=4, separators=(',', ': ')))

        # Send the message that the author gave love to the user mentioned.
        await ctx.send(ctx.author.mention + " gives a love to " + user.mention + " " + regEmoj["g_love"])

    @commands.command()
    async def dailychips(self, ctx, arg=None):
        if arg is not None:
            await ctx.send(embed=Settings.OnErrorMessage('chips', 1))
            return
        chips = random.randint(15, 25)

        # Change the author id.
        author = Settings.ChangeAuthorID(ctx)

        # Add the author to the allowance json.
        Settings.CheckNameInJson(author, profJsonPath, ChipAllowance, "Daily_Chips", 0)

        # Check the allowance of the author.
        if ChipAllowance[author] == 0:
            with open(dailyChipsPath, 'w') as file:
                ChipAllowance[author] = 1
                file.write(json.dumps(ChipAllowance, sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            await ctx.send(embed=Settings.OnErrorMessage('dailychips', 3))
            return

        # Add the author to the chips json.
        Settings.CheckNameInJson(author, profJsonPath, ChipsDic, "Chips", 0)

        with open(chipsPath, 'w') as file:
            # Add the chips to the author.
            ChipsDic[author] += chips
            file.write(json.dumps(ChipsDic, sort_keys=True, indent=4, separators=(',', ': ')))

        # Send the message that the author got their chips.
        await ctx.send(ctx.author.mention + " you get " + str(chips) + " chips.")

    @commands.command()
    async def givechips(self, ctx, arg1=None, arg2=None):
        # Check if arg1 is valid.
        if not await IsARGValid(ctx, arg1, "givechips"):
            return

        # Check if arg2 is valid and a number.
        if arg2 is None:
            await ctx.send(embed=Settings.OnErrorMessage('givechips', 0))
            return
        elif not arg2.isdigit():
            await ctx.send(embed=Settings.OnErrorMessage('givechips', 1))
            return

        # Change the author id.
        author = Settings.ChangeAuthorID(ctx)

        # Change the arg.
        user = await Settings.ChangeArgToUser(ctx, arg1)

        if author not in ChipsDic:
            errorEmbed = discord.Embed(title="Y'shtola found an issue.",
                                       description="You can't give any chips since you don't have any.",
                                       color=Settings.generalColorEMB)
            errorEmbed.set_thumbnail(url=Settings.botIcon)
            await ctx.send(embed=errorEmbed)
            return
        Settings.CheckNameInJson(user.mention.replace('!', ''), profJsonPath, ChipsDic, "Chips", 0)

        # Change the values of the chips if the author has them.
        if ChipsDic[author] >= int(arg2):
            with open(chipsPath, 'w') as file:
                ChipsDic[author] -= int(arg2)
                ChipsDic[user.mention.replace('!', '')] += int(arg2)
                file.write(json.dumps(ChipsDic, sort_keys=True, indent=4, separators=(',', ': ')))

        # Send an error message that you don't have the amount of chips to give.
        else:
            errorEmbed = discord.Embed(title="Y'shtola found an issue.",
                                       description="You can't give " + arg2 + " chips since you have " + str(
                                           ChipsDic[author]),
                                       color=Settings.generalColorEMB)
            errorEmbed.set_thumbnail(url=Settings.botIcon)
            await ctx.send(embed=errorEmbed)
            return

        # Send the message that the author gave chips to the user mentioned.
        await ctx.send(ctx.author.mention + " gives " + arg2 + " chips to " + user.mention)

    @commands.command()
    async def profile(self, ctx, arg=None):
        if arg is not None:
            await ctx.send(embed=Settings.OnErrorMessage('profile', 2))
            return
        # Change the author id.
        author = Settings.ChangeAuthorID(ctx)
        embed = discord.Embed(title="**" + ctx.author.display_name + "**",
                              description="",
                              color=Settings.generalColorEMB)
        embed.add_field(name="Joined on:", value=ctx.author.joined_at.strftime("%b %d, %Y"), inline=False)
        embed.add_field(name="Created on:", value=ctx.author.created_at.strftime("%b %d, %Y"), inline=False)

        loves = 0
        if author in LovesDic:
            loves = LovesDic[author]
        embed.add_field(name="Love:", value=loves, inline=False)

        chips = 0
        if author in ChipsDic:
            chips = ChipsDic[author]
        embed.add_field(name="Chips:", value=chips, inline=False)

        embed.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def refreshDaily(self, ctx):
        # Change the author id.
        author = Settings.ChangeAuthorID(ctx)

        if author != IDsDic["Kon"]:
            await ctx.message.delete()
            return
        JsonUpdate(dailyLovePath, LoveAllowance)
        JsonUpdate(dailyChipsPath, ChipAllowance)

        await ctx.message.delete()

    @commands.command()
    async def loveldr(self, ctx):
        # Set the title.
        title = "Loves leaderboard " + regEmoj["g_love"]

        # Send the message.
        await ctx.send(embed=GetLdr(lovePath, title))

    @commands.command()
    async def chipldr(self, ctx):
        # Set the title.
        title = "Chips leaderboard " + regEmoj["g_cookie"]

        # Send the message.
        await ctx.send(embed=GetLdr(chipsPath, title))

    async def GiveData(bot, message):
        if message.author.mention.replace('!', '') != IDsDic["Kon"]:
            return
        if message.content != "profile-data":
            return

        with open(dailyLovePath) as f:
            LoveAllowance = json.load(f)
        with open(lovePath) as f:
            LovesDic = json.load(f)
        with open(dailyChipsPath) as f:
            ChipAllowance = json.load(f)
        with open(chipsPath) as f:
            ChipsDic = json.load(f)

        channel = 840208543097159690

        await bot.get_channel(channel).send(GetJsonData(LoveAllowance, "Love allowance"))
        await bot.get_channel(channel).send(GetJsonData(LovesDic, "Loves"))
        await bot.get_channel(channel).send(GetJsonData(ChipAllowance, "Chip allowance"))
        await bot.get_channel(channel).send(GetJsonData(ChipsDic, "Chips"))


def setup(client):
    client.add_cog(Discord_prof(client))
