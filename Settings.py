import discord

import json


def init():
    # Test channels.
    global serverText
    serverText = 824706330237075476
    global testGround
    testGround = 824436047593209858

    # Ysthola links server id.
    global ystholaLinksID
    ystholaLinksID = 826820702480891914

    global ffxivannounChann
    ffxivannounChann = 836525085224730654

    global botIcon
    botIcon = "https://cdn.discordapp.com/attachments/826820702480891917/826820786919571456/unknown.png"
    global ARRIcon
    ARRIcon = "https://cdn.discordapp.com/attachments/863357000598814720/863357409682784276/A_Realm_Reborn.jpg"
    global HWIcon
    HWIcon = "https://cdn.discordapp.com/attachments/863357000598814720/863357873581326356/Heavensward.jpg"
    global SBIcon
    SBIcon = "https://cdn.discordapp.com/attachments/863357000598814720/863360386597388298/Stormblood.jpg"
    global ShBIcon
    ShBIcon = "https://cdn.discordapp.com/attachments/863357000598814720/863360422199296030/Shadowbringers.jpg"
    global EWIcon
    EWIcon = "https://cdn.discordapp.com/attachments/863357000598814720/967491126456098916/FFXIV_Endwalker.jpg"

    global generalColorEMB
    generalColorEMB = 0xb266ff

    global RegEmojDic
    with open("Emoj/RegEmoj.json") as f:
        RegEmojDic = json.load(f)

    global AnimatedEmojDic
    with open("Emoj/AnimatedEmoj.json") as f:
        AnimatedEmojDic = json.load(f)

    global IDsDic
    with open("IDs.json") as f:
        IDsDic = json.load(f)

    global smolIDs
    with open("SmolIDs.json") as f:
        smolIDs = json.load(f)

    global admins
    admins = [IDsDic["Kon"], IDsDic["Shiroi"], IDsDic["Lili"], IDsDic["Mid"]]


def OnErrorMessage(commandName, numOfIssue):  # NOTE call this like await ctx.send(embed=OnErrorMessage('command', 0))
    errorMessages = ["You have to provide a valid argument for this command. Check in help for " + commandName,
                     "I could not invoke the argument you gave. Check in help for " + commandName,
                     "You cannot tag yourself or a bot in this command. Check in help for " + commandName,
                     "You already did " + commandName + " today."]
    errorEmbed = discord.Embed(title="Y'shtola found an issue.",
                               description=errorMessages[numOfIssue],
                               color=generalColorEMB)
    errorEmbed.set_thumbnail(url=botIcon)
    return errorEmbed


# TODO remove this function.
def CheckNameInJson(name, folderName, dicName, jsonName, value):
    if name not in dicName:
        with open(folderName + "/" + jsonName + ".json", 'w') as file:
            dicName.update({name: value})
            file.write(json.dumps(dicName, sort_keys=True, indent=4, separators=(',', ': ')))


def RemoveExclaFromID(arg):
    return arg.replace('!', '')


def RemoveAllFromID(arg):
    return arg.replace("<", "").replace("@", "").replace(">", "").replace("!", "")


# NOTE remember to await these functions.
async def ChangeArgToUser(ctx, arg):
    id = RemoveAllFromID(arg)
    return await ctx.guild.fetch_member(id)


async def CommandUnderConstruction(ctx, mes):  #
    await ctx.send(mes + " is under construction.")


async def PurgeMessages(bot, channel, amount=5):
    chan = await bot.fetch_channel(channel)  # get_channel
    await chan.purge(limit=amount)


async def GetMessageFromID(bot, channel, messageID):
    guild = bot.get_guild(ystholaLinksID)
    channel = guild.get_channel(channel)
    return await channel.fetch_message(messageID)


async def GetMember(bot, guildID, user_id):
    # Get the guild.
    guild = discord.utils.find(lambda g: g.id == guildID, bot.guilds)
    # Get the member.
    member = await guild.fetch_member(user_id)
    return member


async def GetRole(bot, guildID, roleName):
    # Get the guild.
    guild = discord.utils.find(lambda g: g.id == guildID, bot.guilds)
    # Get the role.
    role = discord.utils.get(guild.roles, name=roleName)
    return role


async def GetMemberAndRole(bot, guildID, user_id, roleName):
    # Get the member.
    member = await GetMember(bot, guildID, user_id)
    # Get the role.
    role = await GetRole(bot, guildID, roleName)
    return member, role

