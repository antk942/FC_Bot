import json

import random

import discord

import Settings

Settings.init()
IDsDic = Settings.IDsDic


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

    """# Get the description.
    description = ""
    if "description" in frDict:
        description = frDict["description"]"""

    # Get the url.
    picture = ""
    if "image" in frDict:
        if "url" in frDict["image"]:
            picture = frDict["image"]["url"]

    # Set the embed details.
    newEmbd = discord.Embed(title=title, url=url, description=description, color=Settings.generalColorEMB)
    if picture:
        # Set the embed url.
        newEmbd.set_image(url=picture)

    await bot.get_channel(frChannelFC).send(embed=newEmbd)


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
    picture = "https://cdn.discordapp.com/attachments/837628182244622337/837628637670146048/Cactpot.png"
    # Set the embed details.
    newEmbd = discord.Embed(title=title, description=description, color=Settings.generalColorEMB)
    # Set the embed url.
    newEmbd.set_image(url=picture)
    # Set the bot icon.
    newEmbd.set_thumbnail(url=Settings.botIcon)
    await bot.get_channel(channel).send(embed=newEmbd)


async def Lodestone():
    return
