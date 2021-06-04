import json

import random

import discord

import Settings

Settings.init()
IDsDic = Settings.IDsDic


def MakeEmbedOutOfMessage(message):
    diction = message.embeds[0].to_dict()

    title = ""
    # Get the title.
    if "title" in diction:
        title = diction["title"]

    # Get the url.
    url = ""
    if "url" in diction:
        url = diction["url"]

    description = ""
    # Get the description.
    if "description" in diction:
        description = diction["description"]

    # Get the url picture.
    picture = ""
    if "image" in diction:
        if "url" in diction["image"]:
            picture = diction["image"]["url"]

    # Set the embed details.
    newEmbd = discord.Embed(title=title, url=url, description=description, color=Settings.generalColorEMB)

    # Add fields.
    if "fields" in diction:
        for i in range(0, len(diction["fields"])):
            newEmbd.add_field(name=diction["fields"][i]["name"], value=diction["fields"][i]["value"], inline=False)

    # If a picture is found.
    if picture:
        # Set the embed url.
        newEmbd.set_image(url=picture)

    return newEmbd


async def Ffxiv_Lodestone(bot, message):
    # Announcement channels.
    annouFC = Settings.ffxivannounChann
    annouYD = 840517071079079966

    # Check if the message is an embed and in the correct channel.
    if message.channel.id != annouYD or len(message.embeds) == 0:
        return

    # Make the embed.
    newEmbd = MakeEmbedOutOfMessage(message)

    await bot.get_channel(annouFC).send(embed=newEmbd)


async def FashionReport(bot, message):
    # Fashion channels.
    frChannelFC = 835872021057372210
    frChannelYD = 835816641441955860

    newEmbd = discord.Embed

    if message.channel.id != frChannelYD or len(message.embeds) == 0:
        return

    frDict = message.embeds[0].to_dict()

    # Get the title.
    title = ""
    if "title" in frDict:
        lis = frDict["title"].split(" ")
        title = lis[0] + " " + lis[1] + " " + lis[2] + " " + lis[3] + "."

    # Get the url.
    url = ""
    if "url" in frDict:
        url = frDict["url"]

    # Get the description.
    description = "\u200b"

    # Get the url picture.
    picture = ""
    if "image" in frDict:
        if "url" in frDict["image"]:
            picture = frDict["image"]["url"]

    # Set the embed details.
    newEmbd = discord.Embed(title=title, url=url, description=description, color=Settings.generalColorEMB)

    if picture:
        # Set the embed url.
        newEmbd.set_image(url=picture)

    await bot.get_channel(frChannelFC).send(content="<@&841948309971402802>", embed=newEmbd)


async def WeeklyReset(bot, message):
    if message.author.mention.replace('!', '') != IDsDic["Kon"]:
        return

    if message.content != "WR 1409":
        return

    channel = Settings.ffxivannounChann
    title = "*Weekly reset happened.*"
    url = "https://cdn.discordapp.com/attachments/837628182244622337/839100220100968468/panda.png"
    description = "What reset?\n" \
                  "Tomestone cap.\n" \
                  "Alliance raid.\n" \
                  "Challenge log.\n" \
                  "Masked carnival.\n" \
                  "Wonderous tails.\n" \
                  "Custom deliveries.\n" \
                  "Squadron priority mission."

    picture = "https://cdn.discordapp.com/attachments/826820702480891917/826820786919571456/unknown.png"

    # Set the embed details.
    newEmbd = discord.Embed(title=title, url=url, description=description, color=Settings.generalColorEMB)
    # Set the embed url.
    newEmbd.set_image(url=picture)
    # Set footer text.
    newEmbd.set_footer(text="Click the title link.")

    await bot.get_channel(channel).send(embed=newEmbd)


async def Cackpot(bot, message):
    if message.author.mention.replace('!', '') != IDsDic["Kon"]:
        return

    if message.content != "WC 1409":
        return

    channel = Settings.ffxivannounChann
    title = "**Weekly cackpot reminder**"
    description = "Making sure you got your weekly tickets."
    picture = "https://cdn.discordapp.com/attachments/837628182244622337/849317130452598794/2021-06-01_17-01-16-497_TheFashionista_-_Koji.png"
    # Set the embed details.
    newEmbd = discord.Embed(title=title, description=description, color=Settings.generalColorEMB)
    # Set the embed url.
    newEmbd.set_image(url=picture)
    # Set the bot icon.
    newEmbd.set_thumbnail(url=Settings.botIcon)
    await bot.get_channel(channel).send(content="<@&841948309971402802>", embed=newEmbd)


async def Lodestone():
    return
