import json

import random

import discord
from discord.ext import commands

import Settings

Settings.init()
IDsDic = Settings.IDsDic

# region ** NOTE: Jsons locations. ** #
hugLoc = "Jsons_Social/Hug.json"
hugSmolLoc = "Jsons_Social/HugSmol.json"

kissLoc = "Jsons_Social/Kiss.json"

patLoc = "Jsons_Social/Pat.json"
patSmolLoc = "Jsons_Social/PatSmol.json"

lickLoc = "Jsons_Social/Lick.json"

pokeLoc = "Jsons_Social/Poke.json"
pokeSmolLoc = "Jsons_Social/PokeSmol.json"

biteLoc = "Jsons_Social/Bite.json"
biteSmolLoc = "Jsons_Social/BiteSmol.json"

cryLoc = "Jsons_Social/Cry.json"
crySmolLoc = "Jsons_Social/CrySmol.json"

clapLoc = "Jsons_Social/Clap.json"
clapSmolLoc = "Jsons_Social/ClapSmol.json"

angryLoc = "Jsons_Social/Angry.json"
angrySmolLoc = "Jsons_Social/AngrySmol.json"


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
        if author == IDsDic["Lusa"]:
            title = None
            description = author + " hugs " + arg
            command = "HugSmol"
            loc = hugSmolLoc
        else:
            title = None
            description = author + " hugs " + arg
            command = "Hug"
            loc = hugLoc

        await SendEmbed(ctx, loc, title, description, command)

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
        changedArg = Settings.RemoveExclaFromID(arg)
        if changedArg == IDsDic["Lusa"]:
            title = None
            description = author + " pats " + arg
            command = "PatSmol"
            loc = patSmolLoc
        else:
            title = None
            description = author + " pats " + arg
            command = "Pat"
            loc = patLoc

        await SendEmbed(ctx, loc, title, description, command)

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
        if author == IDsDic["Lusa"]:
            title = None
            description = author + " pokes " + arg
            command = "PokeSmol"
            loc = pokeSmolLoc
        else:
            title = None
            description = author + " pokes " + arg
            command = "Poke"
            loc = pokeLoc

        await SendEmbed(ctx, loc, title, description, command)

    @commands.command()
    async def bite(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)
        if author == IDsDic["Lusa"]:
            title = None
            description = author + " bites " + arg
            command = "BiteSmol"
            loc = biteSmolLoc
        else:
            title = None
            description = author + " bites " + arg
            command = "Bite"
            loc = biteLoc

        await SendEmbed(ctx, loc, title, description, command)

    @commands.command()
    async def cry(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)
        if author == IDsDic["Lusa"]:
            title = None
            description = author + " cries because of " + arg
            command = "CrySmol"
            loc = crySmolLoc
        else:
            title = None
            description = author + " cries because of " + arg
            command = "Cry"
            loc = clapLoc

        await SendEmbed(ctx, loc, title, description, command)

    @commands.command()
    async def clap(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)
        if author == IDsDic["Lusa"]:
            title = None
            description = author + " claps for " + arg
            command = "ClapSmol"
            loc = clapSmolLoc
        else:
            title = None
            description = author + " claps for " + arg
            command = "Clap"
            loc = clapLoc

        await SendEmbed(ctx, loc, title, description, command)

    @commands.command()
    async def angry(self, ctx, arg=defArg):
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)
        if author == IDsDic["Lusa"]:
            title = None
            description = author + " is angry at " + arg
            command = "AngrySmol"
            loc = angrySmolLoc
        else:
            title = None
            description = author + " is angry at " + arg
            command = "Angry"
            loc = angryLoc

        await SendEmbed(ctx, loc, title, description, command)
    # endregion


def setup(bot):
    bot.add_cog(Social(bot))
