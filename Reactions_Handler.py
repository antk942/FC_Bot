import discord
from discord.ext import commands

import asyncio

import Reactions_Handler_Functions

import Settings

Settings.init()

roleReacMessageID = 841955569153998888
roleReacChannel = 841952676317233182

channelOfEvents = 860912833697153046
messageOfEvents = 866245165231505428

tank = "<:Tank:867150256435888149>"
healer = "<:Healer:867150256043065355>"
dps = "<:Dps:867150256176889856>"
lateEmoj = "<:Late:866367570046484483>"

emojis = [dps, tank, healer, lateEmoj]


class Reactions_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    isBot = False

    recentReactors = set()
    recentUnreactors = set()

    async def ChangeFieldValues(self, msg, member, emojisAndListsOfEvents, mainKey):
        for key in emojisAndListsOfEvents:
            if key == mainKey:
                if member.mention not in emojisAndListsOfEvents[key][1]:
                    emojisAndListsOfEvents[key][1].append(member.mention)
            elif key != "late":
                if mainKey != "late":
                    if member.mention in emojisAndListsOfEvents[key][1]:
                        emojisAndListsOfEvents[key][1].remove(member.mention)
                    self.isBot = True
                    await msg.remove_reaction(emojisAndListsOfEvents[key][0], member)
                    self.isBot = False

    async def HandleEventReactionsOnAdd(self, msg, payload, member):
        diction = msg.embeds[0].to_dict()
        newEmbed = await Reactions_Handler_Functions.SameFieldsEMB(diction)

        tankLis = diction["fields"][3]["value"].split("\n")
        healerLis = diction["fields"][4]["value"].split("\n")
        dpsLis = diction["fields"][5]["value"].split("\n")
        lateLis = diction["fields"][6]["value"].split("\n")

        listsList = [tankLis, healerLis, dpsLis, lateLis]
        emojisAndListsOfEvents = {
            "tank": (tank, listsList[0]),
            "healer": (healer, listsList[1]),
            "dps": (dps, listsList[2]),
            "late": (lateEmoj, listsList[3])
        }
        mainKey = Reactions_Handler_Functions.ChooseKey(payload.emoji.name)
        await self.ChangeFieldValues(msg, member, emojisAndListsOfEvents, mainKey)
        return Reactions_Handler_Functions.ReturnFieldsForEmbOnAdd(newEmbed, listsList, diction)

    async def HandleEventReactionsOnRemove(self, msg, payload, member):
        diction = msg.embeds[0].to_dict()
        newEmbed = await Reactions_Handler_Functions.SameFieldsEMB(diction)

        tankLis = diction["fields"][3]["value"].split("\n")
        healerLis = diction["fields"][4]["value"].split("\n")
        dpsLis = diction["fields"][5]["value"].split("\n")
        late = diction["fields"][6]["value"].split("\n")

        listsList = [tankLis, healerLis, dpsLis, late]
        emojisAndListsOfEvents = {
            "tank": (tank, listsList[0]),
            "healer": (healer, listsList[1]),
            "dps": (dps, listsList[2]),
            "late": (lateEmoj, listsList[3])
        }
        ret = Reactions_Handler_Functions.RemoveUserFromList(member, emojisAndListsOfEvents, payload.emoji)
        if ret == "All":
            for key in emojisAndListsOfEvents:
                self.isBot = True
                await msg.remove_reaction(emojisAndListsOfEvents[key][0], member)
                self.isBot = False
                await asyncio.sleep(2)

        return Reactions_Handler_Functions.ReturnFieldsForEmbOnRemove(newEmbed, listsList, diction)

    @commands.command()
    async def SendReactionRoleEMB(self, ctx):

        embed = Reactions_Handler_Functions.MakeRoleReactionEMB()

        message = await self.bot.get_channel(roleReacChannel).send(content="@everyone", embed=embed)

        await message.add_reaction("<:Trials:841780257571995700>")
        await message.add_reaction("<:Raids:841780257480638474>")
        await message.add_reaction("<:TreasureHunt:841780257451409419>")
        await message.add_reaction("<:GoldenSaucer:841780257274593281>")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Check if the bot is ready.
        if not self.bot.is_ready():
            return

        msgId = payload.message_id

        # Get the member.
        member = await Settings.GetMember(self.bot, payload.guild_id, str(payload.user_id))
        if member.bot is True:
            return

        msg = await Reactions_Handler_Functions.GetMessageFromPayload(self.bot, payload.guild_id, payload.channel_id,
                                                                      msgId)

        if member in self.recentReactors:
            await msg.remove_reaction(payload.emoji, member)
            self.isBot = True
            return
        else:
            self.recentReactors.add(member)

        # Check if the reacted message is the role reaction.
        if msgId == roleReacMessageID:
            # Get the role.
            role = await Settings.GetRole(self.bot, payload.guild_id, payload.emoji.name)
            if await Reactions_Handler_Functions.GiveRole(member, role) == "Error":
                await msg.clear_reaction(payload.emoji)
        elif str(msgId) in await Reactions_Handler_Functions.GetEventsIDs(self.bot, channelOfEvents, messageOfEvents):
            if str(payload.emoji) not in emojis:
                await msg.clear_reaction(payload.emoji)
                return
            newEmbed = await self.HandleEventReactionsOnAdd(msg, payload, member)
            newEmbed.set_thumbnail(url=Settings.botIcon)
            await msg.edit(embed=newEmbed)

        self.recentReactors.remove(member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if self.isBot:
            self.isBot = False
            return

        msgId = payload.message_id

        # Check if the bot is ready.
        if not self.bot.is_ready():
            return

        # Get the member.
        member = await Settings.GetMember(self.bot, payload.guild_id, str(payload.user_id))
        if member.bot is True:
            return

        msg = await Reactions_Handler_Functions.GetMessageFromPayload(self.bot, payload.guild_id, payload.channel_id,
                                                                      msgId)
        if member in self.recentUnreactors:
            return
        else:
            self.recentUnreactors.add(member)

        # Check if the reacted message is the role reaction..
        if msgId == roleReacMessageID:
            # Get the role.
            role = await Settings.GetRole(self.bot, payload.guild_id, payload.emoji.name)
            # Check the role.
            await Reactions_Handler_Functions.RemoveRole(member, role)
        elif str(msgId) in await Reactions_Handler_Functions.GetEventsIDs(self.bot, channelOfEvents, messageOfEvents):
            newEmbed = await self.HandleEventReactionsOnRemove(msg, payload, member)
            newEmbed.set_thumbnail(url=Settings.botIcon)
            await msg.edit(embed=newEmbed)

        self.isBot = False
        self.recentUnreactors.remove(member)


def setup(bot):
    bot.add_cog(Reactions_Handler(bot))
