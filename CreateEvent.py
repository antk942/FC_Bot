import datetime
import time

import discord
from discord.ext import commands

import CreateEventFunctions

import Settings

Settings.init()
permRole = "newrole"
privacyLink = "https://cdn.discordapp.com/attachments/841303438352711747/853645635245178890/Privacy_Settings.gif"

# Ysthola links ID.
ystholaLinksID = Settings.ystholaLinksID
eventsIDSchannel = 860912833697153046
msgIDs = 866245165231505428


def Commands():
    commList = [
        "clear"
    ]

    commsExplanation = {
        "createevent": ["Create an event for any use.",
                        "$createevent"],
        "deleteevent": ["Delete an event with the id you have from your dms. Make sure to use the command where the event is.",
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
        channels = [830135464526610532, 855136480120143912, 836524035059744778, 824706330237075476, 824436047593209858, 826820702480891917]
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

        # Description.
        description = await CreateEventFunctions.GetMessageResponse(self.bot, ctx, "Create event",
                                                                    "Enter a description for your event.")
        if description is None:
            return

        # Date.
        dateNow = time.strftime("%e-%m-%Y", time.gmtime())
        dateSplit = dateNow.split("-")
        dateNFixed = datetime.datetime(int(dateSplit[2]), int(dateSplit[1]), int(dateSplit[0]))
        dateGot = await CreateEventFunctions.GetCorrectTime(self.bot, ctx, "date.\nExample: 31-12-2021", dateNFixed,
                                                            "date", False, "-", 3)
        if dateGot is None:
            return

        # Time.
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

        await msg.add_reaction("<:Accept:866367570315706378>")
        await msg.add_reaction("<:Decline:866367570340610068>")
        await msg.add_reaction("<:Late:866367570046484483>")
        await CreateEventFunctions.SaveEventID(self.bot, msg, ctx)

    @commands.command()
    async def deleteevent(self, ctx, arg):
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
