import discord

import json


def init():
    # Test channels.
    global serverText
    serverText = 824706330237075476
    global testGround
    testGround = 824436047593209858

    global ffxivannounChann
    ffxivannounChann = 836525085224730654

    global botIcon
    botIcon = "https://cdn.discordapp.com/attachments/826820702480891917/826820786919571456/unknown.png"

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


def CheckNameInJson(name, folderName, dicName, jsonName, value):
    if name not in dicName:
        with open(folderName + "/" + jsonName + ".json", 'w') as file:
            dicName.update({name: value})
            file.write(json.dumps(dicName, sort_keys=True, indent=4, separators=(',', ': ')))


def ChangeAuthorID(ctx):
    return ctx.author.mention.replace('!', '')


async def ChangeArgToUser(ctx, arg):  # NOTE remember to await this function.
    id = arg.replace("<", "").replace("@", "").replace(">", "").replace("!", "")
    return await ctx.guild.fetch_member(id)
