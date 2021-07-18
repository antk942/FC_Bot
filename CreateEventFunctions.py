import datetime
import time

import discord

import Settings

Settings.init()
# Ysthola links ID.
ystholaLinksID = Settings.ystholaLinksID
eventsIDSchannel = 860912833697153046
msgIDs = 866245165231505428


# NOTE: Event creation functions.
def isDatePos(dateGot, currT):
    splitDG = dateGot.split("-")
    datG = [int(splitDG[0]), int(splitDG[1]), int(splitDG[2])]

    try:
        datetime.datetime(datG[2], datG[1], datG[0])
    except ValueError:
        return False

    maxDate = datetime.datetime(year=2022, month=1, day=1)
    dateGotObj = datetime.datetime(datG[2], datG[1], datG[0])
    if dateGotObj < currT or dateGotObj > maxDate:
        return False

    return True


def isTimePos(timeGot, currT, sameD):
    tim = timeGot.split(":")
    if int(tim[0]) > 24 or int(tim[1]) > 59:
        return False
    if sameD:
        if int(timeGot.replace(":", "")) <= int(currT.replace(":", "")):
            return False
    return True


def IsTimeDigit(timeGot, spliter, sizeOfT):
    if not timeGot.replace(spliter, "").isdigit() or len(timeGot.split(spliter)) != sizeOfT:
        return False
    return True


def MakeEmbNoVideo(title, desc):
    emb = discord.Embed(title=title, description="**" + desc + "**",
                        color=Settings.generalColorEMB)
    emb.set_thumbnail(url=Settings.botIcon)
    emb.set_footer(text="Type cancel anytime to end this process.\n"
                        "2 mins of no response will also result to ending this process.")
    return emb


async def CheckResponse(author, resp):
    if resp.lower() == "cancel":
        embed = discord.Embed(title="Creation of this event was canceled.", color=Settings.generalColorEMB)
        embed.set_thumbnail(url=Settings.botIcon)
        await author.send(embed=embed)
        return True
    return False


async def GetMessageResponse(bot, ctx, title, desc):
    newEmb = MakeEmbNoVideo(title, desc)
    await ctx.author.send(embed=newEmb)

    timeout = 120

    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.channel.DMChannel)

    try:
        response = await bot.wait_for('message', timeout=timeout, check=check)
        cont = response.content
        if await CheckResponse(ctx.author, cont):
            return None
        return cont
    except:
        embednew = discord.Embed(title="**Event creation timed out**",
                                 description="Try again.",
                                 color=Settings.generalColorEMB)
        embednew.set_thumbnail(url=Settings.botIcon)
        await ctx.author.send(embed=embednew)
        return None


async def GetCorrectTime(bot, ctx, descD, timeNow, check, sameD, spliter, sizeOfT):
    while True:
        timeGot = await GetMessageResponse(bot, ctx, "Create event", "Enter a correct " + descD)
        if timeGot is None:
            return None

        if not IsTimeDigit(timeGot, spliter, sizeOfT):
            continue

        if check == "date":
            if not isDatePos(timeGot, timeNow):
                continue
        elif check == "time":
            if not isTimePos(timeGot, timeNow, sameD):
                continue

        return timeGot


async def GetMessage(bot, guildID, channelID, msgID):
    guild = bot.get_guild(guildID)
    channel = guild.get_channel(channelID)
    message = await channel.fetch_message(msgID)
    return message


async def SaveEventID(bot, msg, ctx):
    message = await GetMessage(bot, ystholaLinksID, eventsIDSchannel, msgIDs)
    listMess = message.content.split(" ")
    listMess.append(str(msg.id))
    newMessageL = " ".join(listMess)
    await ctx.author.send(content=f"Your event id is: {str(msg.id)}. \nMake sure if you want to delete the event, do the command on the channel where the event is.")
    await message.edit(content=newMessageL)


def SendCreateeventEmbed(ctx, title, description, dateGot, timeGot):
    newEMB = discord.Embed(title=title,
                           description=description,
                           color=Settings.generalColorEMB)
    newEMB.set_thumbnail(url=Settings.botIcon)
    newEMB.add_field(name="Organizer:", value=ctx.author.mention, inline=True)
    newEMB.add_field(name="Date", value=dateGot, inline=True)
    newEMB.add_field(name="Time", value=timeGot + " ST.", inline=True)
    newEMB.add_field(name="Adventurers:", value="\u200b", inline=True)
    newEMB.add_field(name="Declined:", value="\u200b", inline=True)
    newEMB.add_field(name="Late:", value="\u200b", inline=True)
    return newEMB
