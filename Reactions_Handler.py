import discord
from discord.ext import commands

import Reactions_Handler_Functions

import Settings

Settings.init()
IDsDic = Settings.IDsDic

roleReacMessageID = 841955569153998888
roleReacChannel = 841952676317233182

channelOfEvents = 860912833697153046
messageOfEvents = 866245165231505428

adventuresEmoj = "<:Accept:866367570315706378>"
declinedEmoj = "<:Decline:866367570340610068>"
lateEmoj = "<:Late:866367570046484483>"


class Reactions_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    isBot = False
    recentReactors = []

    async def HandleEventReactionsOnAdd(self, msg, payload, member):
        diction = msg.embeds[0].to_dict()
        newEmbed = await Reactions_Handler_Functions.SameFieldsEMB(diction)

        adventures = diction["fields"][3]["value"].split("\n")
        declined = diction["fields"][4]["value"].split("\n")
        late = diction["fields"][5]["value"].split("\n")

        listsList = [adventures, declined, late]
        emojisAndListsOfEvents = {
            "adventures": (adventuresEmoj, listsList[0]),
            "declined": (declinedEmoj, listsList[1]),
            "late": (lateEmoj, listsList[2])
        }
        mainKey = Reactions_Handler_Functions.ChooseKey(payload.emoji.name)
        self.isBot = True
        await Reactions_Handler_Functions.ChangeFieldValues(msg, member, emojisAndListsOfEvents, mainKey)

        return Reactions_Handler_Functions.ReturnFieldsForEmbOnAdd(newEmbed, listsList, diction)

    async def HandleEventReactionsOnRemove(self, msg, payload, member):
        diction = msg.embeds[0].to_dict()
        newEmbed = await Reactions_Handler_Functions.SameFieldsEMB(diction)

        adventures = diction["fields"][3]["value"].split("\n")
        declined = diction["fields"][4]["value"].split("\n")
        late = diction["fields"][5]["value"].split("\n")

        listsList = [adventures, declined, late]
        emojisAndListsOfEvents = {
            "adventures": (adventuresEmoj, listsList[0]),
            "declined": (declinedEmoj, listsList[1]),
            "late": (lateEmoj, listsList[2])
        }
        Reactions_Handler_Functions.RemoveUserFromList(member, emojisAndListsOfEvents, payload.emoji)
        return Reactions_Handler_Functions.ReturnFieldsForEmbOnRemove(newEmbed, listsList, diction)

    @commands.command()
    async def SendReactionRoleEMB(self, ctx):
        if Settings.RemoveExclaFromID(ctx.author.mention) != IDsDic["Kon"]:
            return

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
        # Check if the reacted message is the role reaction.
        if msgId == roleReacMessageID:
            # Get the role.
            role = await Settings.GetRole(self.bot, payload.guild_id, payload.emoji.name)
            await Reactions_Handler_Functions.GiveRole(member, role)
        elif str(msgId) in await Reactions_Handler_Functions.GetEventsIDs(self.bot, channelOfEvents, messageOfEvents):
            newEmbed = await self.HandleEventReactionsOnAdd(msg, payload, member)
            newEmbed.set_thumbnail(url=Settings.botIcon)
            await msg.edit(embed=newEmbed)



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


def setup(bot):
    bot.add_cog(Reactions_Handler(bot))
