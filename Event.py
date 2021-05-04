import discord
from discord.ext import commands
from discord.ext.commands import bot

import Settings

Settings.init()
IDsDic = Settings.IDsDic


def SendEmbedToUser(title):
    newEmbed = discord.Embed(title=title, color=Settings.generalColorEMB)
    newEmbed.set_thumbnail(url=Settings.botIcon)
    newEmbed.set_footer(text="Type *cancel* to end this process.")

    return newEmbed


class Event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def createevent(self, ctx):
        author = Settings.ChangeAuthorID(ctx)
        await ctx.send(embed=SendEmbedToUser("Hello"))


def setup(client):
    client.add_cog(Event(client))
