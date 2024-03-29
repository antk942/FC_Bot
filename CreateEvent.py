import datetime
import time

import discord
from discord.ext import commands

import asyncio

import CreateEventFunctions

import Settings

Settings.init()
IDsDic = Settings.IDsDic
permRole = "newrole"
privacyLink = "https://cdn.discordapp.com/attachments/841303438352711747/853645635245178890/Privacy_Settings.gif"

# Ysthola links ID.
ystholaLinksID = Settings.ystholaLinksID
eventsIDSchannel = 860912833697153046
msgIDs = 866245165231505428


def Commands():
    commList = [
        "createevent",
        "deleteevent"
    ]

    commsExplanation = {
        "createevent": ["Create an event for any use.",
                        "$createevent"],
        "deleteevent": [
            "Delete an event with the id you have from your dms. Make sure to use the command where the event is.",
            "deleteevent <event id>"]
    }

    return commList, commsExplanation


class CreateEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def givePerm(self, ctx, arg):
        # Check if author is the correct one.
        if ctx.author.mention is None:
            return
        rets = await Settings.GetMemberAndRole(self.bot, ystholaLinksID, arg, permRole)
        # Add the role.
        await rets[0].add_roles(rets[1])

    @commands.command()
    async def createevent(self, ctx):
        await ctx.message.delete()
        channels = [860648705215954994, 830135464526610532, 855136480120143912, 836524035059744778, 824706330237075476,
                    824436047593209858, 826820702480891917]
        if ctx.channel.id not in channels:
            return

        try:
            # Title.
            title = await CreateEventFunctions.GetMessageResponse(self.bot, ctx, "Create event",
                                                                  "Enter a title for your event.")
            if title is None:
                return
        except:
            emb = discord.Embed(title="Found an issue.",
                                description=ctx.author.mention + " [make sure i can send you private messages](" +
                                            privacyLink + ")",
                                color=Settings.generalColorEMB)

            emb.set_thumbnail(url=Settings.botIcon)
            await ctx.send(embed=emb)
            return
        if title != "TEST" or Settings.RemoveExclaFromID(ctx.author.mention) != IDsDic["Kon"]:
            # Description.
            description = await CreateEventFunctions.GetMessageResponse(self.bot, ctx, "Create event",
                                                                        "Enter a description for your event.")
            if description is None:
                return

            # Date. dateGot = 31-12-2022
            dateNow = time.strftime("%e-%m-%Y", time.gmtime())
            dateSplit = dateNow.split("-")
            dateNFixed = datetime.datetime(int(dateSplit[2]), int(dateSplit[1]), int(dateSplit[0]))
            dateGot = await CreateEventFunctions.GetCorrectTime(self.bot, ctx, "date.\nExample: 31-12-2022", dateNFixed,
                                                                "date", False, "-", 3)
            if dateGot is None:
                return

            # Time. timeGot = 23:59
            timeNow = time.strftime("%H:%M", time.gmtime())
            sameD = False
            if dateGot == dateNow:
                sameD = True
            timeGot = await CreateEventFunctions.GetCorrectTime(self.bot, ctx, "time in ST.\nExample: 23:59", timeNow,
                                                                "time", sameD, ":", 2)
            if timeGot is None:
                return

            # Role.
            if ctx.guild.id == 824112000342032385:
                availableRoles = ["none", "everyone", "Trials", "Raids", "TreasureHunt"]
            else:
                availableRoles = ["none", "everyone"]
            descrForRoles = ""
            for item in availableRoles:
                descrForRoles += item + "\n"
            roleGot = await CreateEventFunctions.GetMessageResponse(self.bot, ctx, "Enter a role you want to mention.",
                                                                    "```fix\n" + descrForRoles + "```")

            if roleGot is None or roleGot not in availableRoles or roleGot == "none":
                msg = await ctx.send(
                    embed=CreateEventFunctions.SendCreateeventEmbed(ctx, title, description, dateGot, timeGot))
            elif roleGot == "everyone":
                msg = await ctx.send(content="@" + roleGot,
                                     embed=CreateEventFunctions.SendCreateeventEmbed(ctx, title, description, dateGot,
                                                                                     timeGot))
            else:
                if roleGot == "Trials":
                    roleMention = "<@&841947645160325140>"
                elif roleGot == "Raids":
                    roleMention = "<@&841948180258226207>"
                elif roleGot == "TreasureHunt":
                    roleMention = "<@&841947977518022666>"
                msg = await ctx.send(content=roleMention,
                                     embed=CreateEventFunctions.SendCreateeventEmbed(ctx, title, description, dateGot,
                                                                                     timeGot))
        else:
            msg = await ctx.send(embed=CreateEventFunctions.SendCreateeventEmbed(ctx, "test", "test", "11-11-2022",
                                                                                 "23:59"))

        await msg.add_reaction("<:Tank:867150256435888149>")
        await msg.add_reaction("<:Healer:867150256043065355>")
        await msg.add_reaction("<:Dps:867150256176889856>")
        await msg.add_reaction("<:Allrounder:932650649278111754>")
        await msg.add_reaction("<:Late:866367570046484483>")
        await CreateEventFunctions.SaveEventID(self.bot, msg, ctx)

    @commands.command()
    async def deleteevent(self, ctx, arg=None):
        await ctx.message.delete()
        if arg is None:
            msg = await ctx.send(ctx.author.mention + " make sure you add the event id in order to delete it.")
            await asyncio.sleep(5)
            await msg.delete()
            return
        messageEventIDs = await CreateEventFunctions.GetMessage(self.bot, ystholaLinksID, eventsIDSchannel, msgIDs)
        listMess = messageEventIDs.content.split(" ")
        if arg not in listMess:
            return
        listMess.remove(arg)
        newMessageL = " ".join(listMess)
        await messageEventIDs.edit(content=newMessageL)

        msgEvent = await CreateEventFunctions.GetMessage(self.bot, ctx.guild.id, ctx.channel.id, arg)
        await msgEvent.delete()


def setup(bot):
    bot.add_cog(CreateEvent(bot))
