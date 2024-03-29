import discord
from discord.ext import commands

import Settings

Settings.init()

tank = "<:Tank:867150256435888149>"
healer = "<:Healer:867150256043065355>"
dps = "<:Dps:867150256176889856>"
allrounder = "<:Allrounder:932650649278111754>"
lateEmoj = "<:Late:866367570046484483>"


def ChooseKey(emoji):
    if emoji == "Dps":
        return "dps"
    elif emoji == "Tank":
        return "tank"
    elif emoji == "Healer":
        return "healer"
    elif emoji == "Allrounder":
        return "allrounder"
    elif emoji == "Late":
        return "late"


def RemoveUserFromList(member, emojisAndListsOfEvents, emoji):
    for key in emojisAndListsOfEvents:
        if str(emoji) == lateEmoj:
            if member.mention in emojisAndListsOfEvents["late"][1]:
                emojisAndListsOfEvents["late"][1].remove(member.mention)
                return "Late"
        else:
            if member.mention in emojisAndListsOfEvents[key][1]:
                emojisAndListsOfEvents[key][1].remove(member.mention)
    return "All"


def ReturnFieldsForEmbOnAdd(emb, listLists, diction):
    for i in range(0, len(listLists)):
        item = listLists[i]
        if item:
            if item[0] == "\u200b" and len(item) > 1:
                item.remove("\u200b")
        else:
            item.append("\u200b")
        newSTR = "\n".join(item)
        emb.add_field(name=diction["fields"][i + 3]["name"],
                      value=newSTR,
                      inline=True)
    return emb


def ReturnFieldsForEmbOnRemove(emb, listLists, diction):
    for i in range(0, len(listLists)):
        item = listLists[i]
        if not item:
            item.append("\u200b")
        newSTR = "\n".join(item)
        emb.add_field(name=diction["fields"][i + 3]["name"],
                      value=newSTR,
                      inline=True)
    return emb


async def MakeRoleReactionEMB():
    embed = discord.Embed(title="** *Select your role* **", colour=Settings.generalColorEMB,
                          description="These roles are going to be used to notify you at the <#836524035059744778>, <#836525085224730654> and <#835872021057372210> .")

    embed.set_thumbnail(url=Settings.botIcon)

    embed.add_field(name="Role about mount farms.", value="<:Trials:841780257571995700> <@&841947645160325140>",
                    inline=False)
    embed.add_field(name="Role about raids.", value="<:Raids:841780257480638474> <@&841948180258226207>",
                    inline=False)
    embed.add_field(name="Role about treasure hunts.",
                    value="<:TreasureHunt:841780257451409419> <@&841947977518022666>", inline=False)
    embed.add_field(name="Role about golden saucer, FR, cackpot etc.",
                    value="<:GoldenSaucer:841780257274593281> <@&841948309971402802> ", inline=False)
    return embed


async def GiveRole(member, role):
    # Check the role.
    if role is not None:
        # Check the member.
        if member is not None:
            await member.add_roles(role)
            return "Given"
        return "Error"
    else:
        return "Error"


async def RemoveRole(member, role):
    if role is not None:
        # Check the member.
        if member is not None:
            await member.remove_roles(role)


async def GetEventsIDs(bot, channelOfEvents, messageOfEvents):
    msg = await Settings.GetMessageFromID(bot, channelOfEvents, messageOfEvents)
    temp = msg.content.split(" ")
    del temp[0]
    return temp


async def SameFieldsEMB(embDictionary):
    emb = discord.Embed(title=embDictionary["title"], description=embDictionary["description"],
                        color=Settings.generalColorEMB)
    # Same values every time
    emb.add_field(name=embDictionary["fields"][0]["name"],
                  value=embDictionary["fields"][0]["value"],
                  inline=True)
    emb.add_field(name=embDictionary["fields"][1]["name"],
                  value=embDictionary["fields"][1]["value"],
                  inline=True)
    emb.add_field(name=embDictionary["fields"][2]["name"],
                  value=embDictionary["fields"][2]["value"],
                  inline=True)
    # End.
    emb.set_footer(text="Reactions will update every couple of seconds.")
    return emb


async def GetMessageFromPayload(bot, guildId, channel, messageID):
    guild = bot.get_guild(guildId)
    channel = guild.get_channel(channel)
    return await channel.fetch_message(messageID)
