import discord

import Settings

IDsDic = Settings.IDsDic


def FRCheck(message):
    # Test channels.
    serverText = 824706330237075476
    testGround = 824436047593209858
    # Fashion channels.
    frChannelFC = 835872021057372210  # testGround
    frChannelYD = 835816641441955860  # serverText

    allowed = True
    newEmbd = discord.Embed
    
    if message.channel.id == frChannelYD and len(message.embeds) != 0:
        frDict = message.embeds[0].to_dict()
        print(frDict)

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
        description = ""
        if "description" in frDict:
            description = frDict["description"]
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
    else:
        allowed = False

    return allowed, newEmbd, frChannelFC
