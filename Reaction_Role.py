import discord
from discord.ext import commands

import Settings

Settings.init()
IDsDic = Settings.IDsDic

roleReacMessageID = 841955569153998888
roleReacChannel = 841952676317233182


class Reaction_Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def SendReactionRoleEMB(self, ctx):
        if Settings.RemoveExclaFromID(ctx.author.mention) != IDsDic["Kon"]:
            return
        embed = discord.Embed(title="** *Select your role* **", colour=Settings.generalColorEMB,
                              description="These roles are going to be used to notify you at the <#836524035059744778>, <#836525085224730654> and <#835872021057372210> .")

        embed.set_thumbnail(url=Settings.botIcon)

        embed.add_field(name="Role about mount farms.", value="<:Trials:841780257571995700> <@&841947645160325140>",
                        inline=False)
        embed.add_field(name="Role about raids.", value="<:Raids:841780257480638474> <@&841948180258226207>", inline=False)
        embed.add_field(name="Role about treasure hunts.", value="<:TreasureHunt:841780257451409419> <@&841947977518022666>", inline=False)
        embed.add_field(name="Role about golden saucer, FR, cackpot etc.",
                        value="<:GoldenSaucer:841780257274593281> <@&841948309971402802> ", inline=False)

        message = await self.bot.get_channel(roleReacChannel).send(content="@everyone", embed=embed)

        await message.add_reaction("<:Trials:841780257571995700>")
        await message.add_reaction("<:Raids:841780257480638474>")
        await message.add_reaction("<:TreasureHunt:841780257451409419>")
        await message.add_reaction("<:GoldenSaucer:841780257274593281>")

    async def GetMemberAndRole(self, payload):
        # Get the guild.
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.bot.guilds)
        # Get the role.
        role = discord.utils.get(guild.roles, name=payload.emoji.name)  # Or "new role2" if u need dif names for emojs roles.
        # Get the member.
        member = await guild.fetch_member(str(payload.user_id))
        # Return.
        return role, member

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Check if the bot is ready.
        if not self.bot.is_ready():
            return
        # Check if the reacted message is the correct.
        if payload.message_id != roleReacMessageID:
            return

        rets = await self.GetMemberAndRole(payload)
        # Get the role and member.
        role = rets[0]
        member = rets[1]
        # Check the role.
        if role is None:
            return
        # Check the member.
        if member is None:
            return
        else:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Check if the bot is ready.
        if not self.bot.is_ready():
            return
        # Check if the reacted message is the correct.
        if payload.message_id != roleReacMessageID:
            return

        rets = await self.GetMemberAndRole(payload)
        # Get the role and member.
        role = rets[0]
        member = rets[1]
        # Check the role.
        if role is None:
            return
        # Check the member.
        if member is None:
            return
        else:
            await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Reaction_Role(bot))
