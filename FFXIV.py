import io
import json

import discord
from discord.ext import commands

import Settings

import FFXIV_Functions

ffxivLodestoneIDPath = "Jsons_FFXIV/FFXIV_Lodestone_ID.json"


Settings.init()
ffxivRegEm = Settings.RegEmojDic
ffxivAnimEm = Settings.AnimatedEmojDic


def Commands():
    commList = ["iam",
                "whoami",
                "mylogs",
                "logs"]
    commsExplanation = ["Give a love to someone.",
                        "Get your daily chips.",
                        "Give chips to someone.",
                        "Check out your profile information.",
                        "See who has the most love.",
                        "See who has the most chips."]

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
        # Get the lodestone id from the api.
        lodestoneID = await FFXIV_Functions.GetUserLodestoneID(ctx, arg1, arg2, arg3, 'iam')
        # If the function got an error exit the command.
        if lodestoneID is False:
            return

        # Change author's id.
        author = Settings.ChangeAuthorID(ctx)
        with open(ffxivLodestoneIDPath) as f:
            Lodestone_IDDic = json.load(f)
        # If the author is already saved exit the command.
        if author in Lodestone_IDDic:
            await ctx.send(ctx.author.mention + " you already have saved your character. " + ffxivRegEm["g_blep"])
            return

        # Save the author's lodestone id.
        with open(ffxivLodestoneIDPath, 'w') as file:
            Lodestone_IDDic.update({author: [lodestoneID, arg1, arg2, arg3]})
            file.write(json.dumps(Lodestone_IDDic, sort_keys=True, indent=4, separators=(',', ': ')))
        await ctx.send(ctx.author.mention + " your character is successfully saved. " + ffxivRegEm["g_love"])

    @commands.command()
    async def whoami(self, ctx, arg=None):
        if arg is not None:
            await ctx.send(embed=Settings.OnErrorMessage('whoami', 1))
            return

        # Change author's id.
        author = Settings.ChangeAuthorID(ctx)
        with open(ffxivLodestoneIDPath) as f:
            Lodestone_IDDic = json.load(f)
        # Check if the author has used iam.
        if author not in Lodestone_IDDic:
            await ctx.send(ctx.author.mention + " you have to use $iam to use $whoami. " + ffxivRegEm["g_shock"])
            return
        FFXIV_Functions.CheckIfAuthorInfoChanged(author)

        charID = Lodestone_IDDic[author][0]
        background = "Whoami_FFXIV/Background_Img_Whoami.png"
        font = "Whoami_FFXIV/ferrum.otf"
        jobs = "Whoami_FFXIV/Jobs.png"
        whoamipic = FFXIV_Functions.WhoamiImg(charID, background, jobs, font)

        whoamipic.save("result.png")
        await sendEmbedMessageFile(ctx, None, "", "result.png", "result.png")

    @commands.command()
    async def mylogs(self, ctx, arg=None):
        if arg is not None:
            await ctx.send(embed=Settings.OnErrorMessage('mylogs', 1))
            return
        # Change author's id.
        author = Settings.ChangeAuthorID(ctx)
        with open(ffxivLodestoneIDPath) as f:
            Lodestone_IDDic = json.load(f)
        if author not in Lodestone_IDDic:
            await ctx.send(ctx.author.mention + " you have to use $iam to use $mylogs. " + ffxivRegEm["g_shock"])
            return
        FFXIV_Functions.CheckIfAuthorInfoChanged(author)

        # Set the user and the world for the fflogs site
        user = Lodestone_IDDic[author][1] + " " + Lodestone_IDDic[author][2]
        world = Lodestone_IDDic[author][3]

        # Get the embed.
        embed = await FFXIV_Functions.SendLogs(ctx, user, world)
        # If the function exited return.
        if embed is None:
            return
        await ctx.send(embed=embed)

    @commands.command()
    async def logs(self, ctx, arg1=None, arg2=None, arg3=None):
        # Check if argument is a valid person, not a role or invalid.
        if arg1 is None or arg2 is None or arg3 is None:
            await ctx.send(embed=Settings.OnErrorMessage("logs", 0))
            return
        # Get the embed.
        embed = await FFXIV_Functions.SendLogs(ctx, arg1 + " " + arg2, arg3)
        # If the function exited return.
        if embed is None:
            return
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FFXIV(bot))
