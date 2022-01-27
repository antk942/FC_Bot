import io
import json

import discord
from discord.ext import commands

import Settings

import FFXIV_Functions

ffxivLodestoneIDPath = "Jsons_FFXIV/FFXIV_Lodestone_ID.json"
ffxivCharacterInfoChannel = 858993434642350080
ffxivLodestoneIDsChannel = 858650958106984478
ffxivLodestoneIDsMessage = 872405091540430879

Settings.init()
ffxivRegEm = Settings.RegEmojDic
ffxivAnimEm = Settings.AnimatedEmojDic


def Commands():
    commList = ["iam",
                "whoami",
                "mylogs",
                "logs",
                "mb"]

    commsExplanation = {
        "iam": ["Add your character.",
                "$iam <name + surname + world>"],
        "whoami": ["Check your character details.",
                   "$whoami"],
        "mylogs": ["Check your logs for a different patch or in general.",
                   "$mylogs <none>"],
        "logs": ["Check someones logs for a different patch or in general.",
                 "$logs <name + surname + world>"],  # + <none or 5.5 or 5.4 or echo>
        "mb": ["Check prices for a specific item.",
               "$mb <item name>"]
    }

    return commList, commsExplanation


async def sendEmbedMessageFile(ctx, title, description, filepath, filename):
    embed = discord.Embed(title=title, description=description, color=Settings.generalColorEMB)
    if filepath is not None and filename is not None:
        file = discord.File(filepath)
        embed.set_image(url="attachment://" + filename)
        await ctx.send(file=file, embed=embed)
    else:
        await ctx.send(embed=embed)


class FFXIV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def iam(self, ctx, arg1=None, arg2=None, arg3=None):  # arg1 = name, arg2 = surname, arg3 = world.
        await ctx.message.add_reaction("⏳")
        # Get the lodestone id from the api.
        lodestoneID = await FFXIV_Functions.GetUserLodestoneID(ctx, arg1, arg2, arg3, 'iam')
        # If the function got an error exit the command.
        if lodestoneID is False:
            return

        # Change author's id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)
        lodestoneIDsMes = await Settings.GetMessageFromID(self.bot, ffxivLodestoneIDsChannel, ffxivLodestoneIDsMessage)
        # If the author is already saved exit the command.
        if author in lodestoneIDsMes.content:
            await ctx.send(ctx.author.mention + " you already have saved your character. " + ffxivRegEm["g_blep"])
            return

        await ctx.send(ctx.author.mention + " your character is successfully saved. " + ffxivRegEm["g_love"])
        msg = await self.bot.get_channel(ffxivCharacterInfoChannel).send(lodestoneID + "\n" +
                                                                         arg1 + "\n" +
                                                                         arg2 + "\n" +
                                                                         arg3)
        await FFXIV_Functions.SaveCharacterMesID(self.bot, msg, author)

    @commands.command()
    async def whoami(self, ctx, arg=None):
        await ctx.message.add_reaction("⏳")
        if arg is not None:
            await ctx.send(embed=Settings.OnErrorMessage('whoami', 1))
            return

        # Change author's id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)
        lodestoneIDsMes = await Settings.GetMessageFromID(self.bot, ffxivLodestoneIDsChannel,
                                                              ffxivLodestoneIDsMessage)
        # If the author is already saved exit the command.
        if author not in lodestoneIDsMes.content:
            await ctx.send(ctx.author.mention + " you have to use $iam to use $whoami" + ffxivRegEm["g_blep"])
            return
        await FFXIV_Functions.CheckIfAuthorInfoChanged(self.bot, lodestoneIDsMes, author)

        listOfLodes = lodestoneIDsMes.content.split(" ")
        characterInfoMessID = -1
        for i in range(0, len(listOfLodes)):
            if listOfLodes[i] == author:
                characterInfoMessID = listOfLodes[i + 1]
                break
        mesOfCharacter = await Settings.GetMessageFromID(self.bot, ffxivCharacterInfoChannel, characterInfoMessID)
        listOfCharacterInfo = mesOfCharacter.content.split("\n")
        charID = listOfCharacterInfo[0]
        background = "Whoami_FFXIV/Background_Img_Whoami.png"
        font = "Whoami_FFXIV/ferrum.otf"
        jobs = "Whoami_FFXIV/Jobs.png"
        whoamipic = FFXIV_Functions.WhoamiImg(charID, background, jobs, font)

        whoamipic.save("result.png")
        await sendEmbedMessageFile(ctx, None, "", "result.png", "result.png")

    @commands.command()
    async def mylogs(self, ctx, arg=None):
        await ctx.message.add_reaction("⏳")
        # Get the embed.
        if arg is not None:  # arg != "echo" and arg is not None and arg != "5.5" and arg != "5.4":
            await ctx.send(ctx.author.mention + " something went wrong, check for $help mylogs." + ffxivRegEm["g_blep"])
            return
        # Change author's id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)
        lodestoneIDsMes = await Settings.GetMessageFromID(self.bot, ffxivLodestoneIDsChannel,
                                                              ffxivLodestoneIDsMessage)
        # If the author is already saved exit the command.
        if author not in lodestoneIDsMes.content:
            await ctx.send(ctx.author.mention + " you have to use $iam to use $mylogs" + ffxivRegEm["g_blep"])
            return
        await FFXIV_Functions.CheckIfAuthorInfoChanged(self.bot, lodestoneIDsMes, author)

        listOfLodes = lodestoneIDsMes.content.split(" ")
        characterInfoMessID = -1
        for i in range(0, len(listOfLodes)):
            if listOfLodes[i] == author:
                characterInfoMessID = listOfLodes[i + 1]
                break
        mesOfCharacter = await Settings.GetMessageFromID(self.bot, ffxivCharacterInfoChannel, characterInfoMessID)
        listOfCharacterInfo = mesOfCharacter.content.split("\n")

        # Set the user and the world for the fflogs site
        user = listOfCharacterInfo[1] + " " + listOfCharacterInfo[2]
        world = listOfCharacterInfo[3]

        # Get the embed.
        embed = await FFXIV_Functions.SendLogs(ctx, user, world, arg)
        # If the function exited return.
        if embed is None:
            return
        await ctx.send(embed=embed)

    @commands.command()
    async def logs(self, ctx, arg1=None, arg2=None, arg3=None, arg4=None):
        await ctx.message.add_reaction("⏳")
        # Check if argument is a valid person, not a role or invalid.
        if arg1 is None or arg2 is None or arg3 is None or arg4 is not None:
            await ctx.send(embed=Settings.OnErrorMessage("logs", 0))
            return
        # Get the embed.
        """if arg4 != "echo" and arg4 is not None and arg4 != "5.5" and arg4 != "5.4":
            await ctx.send(ctx.author.mention + " something went wrong, check for $help logs." + ffxivRegEm["g_blep"])
            return"""
        embed = await FFXIV_Functions.SendLogs(ctx, arg1 + " " + arg2, arg3, arg4)
        # If the function exited return.
        if embed is None:
            return
        await ctx.send(embed=embed)

    @commands.command()
    async def mb(self, ctx, *arg):
        await ctx.message.add_reaction("⏳")
        item = ' '.join(arg)
        if not item:
            await ctx.send(embed=Settings.OnErrorMessage("mb", 0))
            return
        retu = await FFXIV_Functions.GetMarketBoardEMB(ctx, item)
        if retu is None:
            return
        await ctx.send(embed=retu)


def setup(bot):
    bot.add_cog(FFXIV(bot))
