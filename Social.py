import json

import random

import discord
from discord.ext import commands

import Settings

Settings.init()
IDsDic = Settings.IDsDic

# region ** NOTE: Jsons locations. ** #
hugLoc = "Jsons_Social/Hug.json"
kissLoc = "Jsons_Social/Kiss.json"
patLoc = "Jsons_Social/Pat.json"
lickLoc = "Jsons_Social/Lick.json"
pokeLoc = "Jsons_Social/Poke.json"
biteLoc = "Jsons_Social/Bite.json"
cryLoc = "Jsons_Social/Cry.json"
clapLoc = "Jsons_Social/Clap.json"
angryLoc = "Jsons_Social/Angry.json"


# endregion


def Commands():
    commList = [
        "hug",
        "kiss",
        "pat",
        "lick",
        "poke",
        "bite",
        "cry",
        "clap",
        "angry"
    ]

    commsExplanation = {
        "hug": ["Hug someone.",
                "$hug <@target>"],
        "kiss": ["Kiss someone.",
                 "$kiss <@target>"],
        "pat": ["Pat someone.",
                "$pat <@target>"],
        "lick": ["Lick someone.",
                 "$lick <@target>"],
        "poke": ["Poke someone.",
                 "$poke <@target>"],
        "bite": ["Bite someone.",
                 "$bite <@target>"],
        "cry": ["Cry because of someone.",
                "$cry <@target>"],
        "clap": ["Clap for someone.",
                 "$clap <@target>"],
        "angry": ["Be angry at someone.",
                  "$angry <@target>"]
    }

    return commList, commsExplanation


async def SendEmbed(ctx, dicLoc, title, description, command):
    # Set the embed details.
    embed = discord.Embed(title=title, description=description, color=Settings.generalColorEMB)
    # embed.set_thumbnail(url=Settings.botIcon)

    # Open the dictionary.
    with open(dicLoc) as file:
        dic = json.load(file)
    if not bool(dic):
        print("dic is empty")
        return
    # Choose a random link.
    x = str(random.randint(0, len(dic) - 1))
    # Set the link.
    embed.set_image(url=dic[command + x])

    await ctx.send(embed=embed)


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def temp(self, ctx):
        if Settings.RemoveExclaFromID(ctx.author.mention) != IDsDic["Kon"]:
            return
        fileLoc = kissLoc
        with open(fileLoc) as file:
            dic = json.load(file)
        print(dict(sorted(dic.items())))

    @commands.command()
    async def addgif(self, ctx, command, link):
        # Check the author before adding.
        if Settings.RemoveExclaFromID(ctx.author.mention) != IDsDic["Kon"]:
            return

        # Open the json file.
        fileLoc = "Jsons_Social/" + command + ".json"
        with open(fileLoc) as file:
            dic = json.load(file)

        # Add the gif based on the size of the dictionary.
        name = command + str(len(dic))
        with open(fileLoc, 'w') as file:
            dic.update({name: link})
            file.write(json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': ')))

    # region ** NOTE: Social commands. ** #.
    defArg = "everyone"

    @commands.command()
    async def hug(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " hugs " + arg
        command = "Hug"

        await SendEmbed(ctx, hugLoc, title, description, command)

    @commands.command()
    async def kiss(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " kisses " + arg
        command = "Kiss"

        await SendEmbed(ctx, kissLoc, title, description, command)

    @commands.command()
    async def pat(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " pats " + arg
        command = "Pat"

        await SendEmbed(ctx, patLoc, title, description, command)

    @commands.command()
    async def lick(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " licks " + arg
        command = "Lick"

        await SendEmbed(ctx, lickLoc, title, description, command)

    @commands.command()
    async def poke(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " pokes " + arg
        command = "Poke"

        await SendEmbed(ctx, pokeLoc, title, description, command)

    @commands.command()
    async def bite(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " bites " + arg
        command = "Bite"

        await SendEmbed(ctx, biteLoc, title, description, command)

    @commands.command()
    async def cry(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " cries because of " + arg
        command = "Cry"

        await SendEmbed(ctx, cryLoc, title, description, command)

    @commands.command()
    async def clap(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " claps for " + arg
        command = "Clap"

        await SendEmbed(ctx, clapLoc, title, description, command)

    @commands.command()
    async def angry(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        title = None
        description = author + " is angry at " + arg
        command = "Angry"

        await SendEmbed(ctx, angryLoc, title, description, command)
    # endregion


def setup(bot):
    bot.add_cog(Social(bot))
