import random

import discord
from discord.ext import commands

import Settings

Settings.init()
IDsDic = Settings.IDsDic
regEmoj = Settings.RegEmojDic

# Ysthola links ID.
ystholaLinksID = Settings.ystholaLinksID

# Ysthola links channels.
dailyLoveChannel = 857230502054461450
lovesChannel = 857230470235815956
dailyChipsChannel = 857230122914545675
chipsChannel = 857230086863978546
backups = 858346558202707978

# Message ids.
dailyLoveID = 860081266648023040
lovesID = 860081340024487956
dailyChipsID = 860081466355875880
chipsID = 860081533636313098


def Commands():
    commList = [
        "love",
        "dailychips",
        "givechips",
        "profile",
        "loveldr",
        "chipldr"
    ]

    commsExplanation = {
        "love": ["Give a love to someone.",
                 "$love <@target> / not a bot or a role"],
        "dailychips": ["Get your daily chips.",
                       "$dailychips"],
        "givechips": ["Give chips to someone.",
                      "$givechips <@target + amount> / not a bot or a role"],
        "profile": ["Check out your profile information.",
                    "$profile"],
        "loveldr": ["See who has the most love.",
                    "$loveldr"],
        "chipldr": ["See who has the most chips.",
                    "$chipldr"]
    }

    return commList, commsExplanation


async def SendMessageBackup(bot, mes):
    await bot.get_channel(backups).send(mes)


async def GetMessageFromID(bot, channel, messageID):
    guild = bot.get_guild(ystholaLinksID)
    channel = guild.get_channel(channel)
    return await channel.fetch_message(messageID)


async def CanAuthorGive(ctx, author, dailyList, message, command):
    # Check if the author is in the list and update it.
    dailyListUpdated = CheckIfPersonInTracker(author, dailyList, 0)
    # Get the index.
    indexOfAllowance = dailyListUpdated.index(author) + 1
    # Get the value.
    dailyNumber = int(dailyListUpdated[indexOfAllowance])
    # Message handler.
    if dailyNumber == 0:
        dailyNumber += 1
        dailyListUpdated[indexOfAllowance] = str(dailyNumber)  # update the value
        newMessageDL = " ".join(dailyListUpdated)
        await message.edit(content=newMessageDL)
        return True
    else:
        # Return an error message that the author already gave today.
        await ctx.send(embed=Settings.OnErrorMessage(command, 3))
        return False


async def ChangeUserValues(userMentioned, comList, extraValue, message):
    # Check if the user is in the list and update it.
    listUpdated = CheckIfPersonInTracker(userMentioned, comList, 0)
    # Get the index.
    indexOfCom = listUpdated.index(userMentioned) + 1
    # Get the value.
    comNumber = int(listUpdated[indexOfCom]) + extraValue
    # Update the message.
    listUpdated[indexOfCom] = str(comNumber)
    newMessageL = " ".join(listUpdated)
    await message.edit(content=newMessageL)


async def MessageUpdate(message):
    dailyList = message.content.split(" ")

    i = 1
    while i < len(dailyList):
        dailyList[i] = "0"
        i += 2

    newMessageL = " ".join(dailyList)
    await message.edit(content=newMessageL)


def CheckIfPersonInTracker(person, messageList, value):
    if person not in messageList:
        messageList.append(person)
        messageList.append(str(value))

    return messageList


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


def GetLdr(message, title):
    messageList = message.content.split(" ")
    valuesList = []
    i = 1
    while i < len(messageList):
        valuesList.append(messageList[i])
        i += 2

    finalList = []
    for i in range(0, 5):
        max1 = 0
        indexOfValue = 1

        for j in range(len(valuesList)):
            if valuesList[j] > max1:
                max1 = valuesList[j]
                indexOfValue = valuesList.index(j)

        valuesList.remove(max1)
        finalList.append(messageList[indexOfValue])
        finalList.append(max1)

    newMessageL = " ".join(finalList)
    # Make the embed.
    ldrEmbed = discord.Embed(title=title,
                             description=newMessageL,
                             color=Settings.generalColorEMB)

    return ldrEmbed


class Discord_prof(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def DailyREF(bot):
        dailyLoveMessage = await GetMessageFromID(bot, dailyLoveChannel, dailyLoveID)
        await MessageUpdate(dailyLoveMessage)

        dailyChipsMessage = await GetMessageFromID(bot, dailyChipsChannel, dailyChipsID)
        await MessageUpdate(dailyChipsMessage)

    @commands.command()
    async def love(self, ctx, arg=None):
        if not await IsARGValid(ctx, arg, "love"):
            return

        # Change the arg.
        user = await Settings.ChangeArgToUser(ctx, arg)

        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        # Daily love allowance handler.
        # Get the message.
        dailyLoveMessage = await GetMessageFromID(self.bot, dailyLoveChannel, dailyLoveID)
        # Split into the components.
        dailyLoveList = dailyLoveMessage.content.split(" ")
        # Check if the author is allowed to give love and or update tracker.
        if not await CanAuthorGive(ctx, author, dailyLoveList, dailyLoveMessage, "love"):
            return

        # Love handler.
        # Replace the ! to the user mentioned.
        userMentioned = user.mention.replace('!', '')
        # Get the message.
        lovesMessage = await GetMessageFromID(self.bot, lovesChannel, lovesID)
        # Split into the components.
        loveList = lovesMessage.content.split(" ")
        # Update tracker.
        await ChangeUserValues(userMentioned, loveList, 1, lovesMessage)

        # Send the message that the author gave love to the user mentioned.
        mes = ctx.author.mention + " gives a love to " + user.mention + " " + regEmoj["g_love"]
        await ctx.send(mes)
        await SendMessageBackup(self.bot, mes)

    @commands.command()
    async def dailychips(self, ctx, arg=None):
        if arg is not None:
            await ctx.send(embed=Settings.OnErrorMessage('chips', 1))
            return
        chips = random.randint(15, 25)

        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        # Daily chip allowance handler.
        # Get the message.
        dailyChipsMessage = await GetMessageFromID(self.bot, dailyChipsChannel, dailyChipsID)
        # Split into the components.
        dailyChipsList = dailyChipsMessage.content.split(" ")
        # Check if the author is allowed to give love and or update tracker.
        if not await CanAuthorGive(ctx, author, dailyChipsList, dailyChipsMessage, "dailychips"):
            return

        # Chips handler.
        # Get the message.
        chipsMessage = await GetMessageFromID(self.bot, chipsChannel, chipsID)
        # Split into the components.
        chipsList = chipsMessage.content.split(" ")
        # Update tracker.
        await ChangeUserValues(author, chipsList, chips, chipsMessage)

        # Send the message that the author got their chips.
        mes = ctx.author.mention + " you get " + str(chips) + " chips."
        await ctx.send(mes)
        await SendMessageBackup(self.bot, mes)

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
        chipsToGive = int(arg2)

        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        # Change the arg.
        user = await Settings.ChangeArgToUser(ctx, arg1)

        # Chips handler.
        # Get the message.
        chipsMessage = await GetMessageFromID(self.bot, chipsChannel, chipsID)
        # Split into the components.
        chipsList = chipsMessage.content.split(" ")

        if author not in chipsList:
            errorEmbed = discord.Embed(title="Y'shtola found an issue.",
                                       description="You can't give any chips since you don't have any.",
                                       color=Settings.generalColorEMB)
            errorEmbed.set_thumbnail(url=Settings.botIcon)
            await ctx.send(embed=errorEmbed)
            return

        # Replace the ! to the user mentioned.
        userMentioned = user.mention.replace('!', '')

        # Get the new list.
        chipsListUpdated = CheckIfPersonInTracker(userMentioned, chipsList, 0)

        # Author values.
        authorIndex = chipsListUpdated.index(author) + 1
        authorChips = int(chipsListUpdated[authorIndex])

        # User values.
        userMentionedIndex = chipsListUpdated.index(userMentioned) + 1
        userChips = int(chipsListUpdated[userMentionedIndex])

        if authorChips >= chipsToGive:
            # Update values.
            chipsListUpdated[authorIndex] = str(authorChips - chipsToGive)
            chipsListUpdated[userMentionedIndex] = str(userChips + chipsToGive)
            # Update message.
            newMessageL = " ".join(chipsListUpdated)
            await chipsMessage.edit(content=newMessageL)
        # Send an error message that you don't have the amount of chips to give.
        else:
            errorEmbed = discord.Embed(
                title="Y'shtola found an issue.",
                description="You can't give " + arg2 + " chips since you have " + str(authorChips),
                color=Settings.generalColorEMB)
            errorEmbed.set_thumbnail(url=Settings.botIcon)
            await ctx.send(embed=errorEmbed)
            return

        # Send the message that the author gave chips to the user mentioned.
        mes = ctx.author.mention + " gives " + arg2 + " chips to " + user.mention
        await ctx.send(mes)
        await SendMessageBackup(self.bot, mes)

    @commands.command()
    async def profile(self, ctx, arg=None):
        if arg is not None:
            await ctx.send(embed=Settings.OnErrorMessage('profile', 2))
            return
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)
        embed = discord.Embed(title="**" + ctx.author.display_name + "**",
                              description="",
                              color=Settings.generalColorEMB)
        embed.add_field(name="Joined on:", value=ctx.author.joined_at.strftime("%b %d, %Y"), inline=False)
        embed.add_field(name="Created on:", value=ctx.author.created_at.strftime("%b %d, %Y"), inline=False)

        # Love field.
        lovesMessage = await GetMessageFromID(self.bot, lovesChannel, lovesID)
        # Split into the components.
        lovesList = lovesMessage.content.split(" ")
        loves = 0
        if author in lovesList:
            indexOfLoves = lovesList.index(author) + 1
            loves = lovesList[indexOfLoves]
        embed.add_field(name="Love:", value=loves, inline=False)

        # Chips field.
        chipsMessage = await GetMessageFromID(self.bot, chipsChannel, chipsID)
        # Split into the components.
        chipsList = chipsMessage.content.split(" ")
        chips = 0
        if author in chipsList:
            indexOfChips = chipsList.index(author) + 1
            chips = chipsList[indexOfChips]
        embed.add_field(name="Chips:", value=chips, inline=False)

        embed.set_thumbnail(url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def refreshDaily(self, ctx):
        await ctx.message.delete()
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        if author != IDsDic["Kon"]:
            return

        await self.DailyREF()

    @commands.command()
    async def loveldr(self, ctx):
        # Set the title.
        title = "Loves leaderboard " + regEmoj["g_love"]
        lovesMessage = await GetMessageFromID(self.bot, lovesChannel, lovesID)
        # Send the message.
        await ctx.send(embed=GetLdr(lovesMessage, title))

    @commands.command()
    async def chipldr(self, ctx):
        # Set the title.
        title = "Chips leaderboard " + regEmoj["g_cookie"]
        chipsMessage = await GetMessageFromID(self.bot, chipsChannel, chipsID)
        # Send the message.
        await ctx.send(embed=GetLdr(chipsMessage, title))


def setup(bot):
    bot.add_cog(Discord_prof(bot))
