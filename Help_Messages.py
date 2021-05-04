import json
import random

import discord
from discord.ext import commands

import Settings

Settings.init()
IDsDic = Settings.IDsDic


class Help_Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

        @commands.command()
        async def help_message_compProjects(ctx):
            await ctx.message.delete()
            if ctx.author.mention.replace('!', '') != IDsDic["Kon"]:
                return
            embed = discord.Embed(title="Company Projects help commands",
                                  description="This is a list of the commands you can use.",
                                  color=Settings.generalColorEMB)
            embed.set_thumbnail(url=Settings.botIcon)
            embed.add_field(name="addrecipe  <Recipe name>", value="Add a recipe to the files it returns a codename.",
                            inline=False)
            embed.add_field(name="clearrecipe <Code name/all>",
                            value="Remove a recipe from the files, or if you type all it will remove all recipes.",
                            inline=False)
            embed.add_field(name="additem <Code name + item>", value="Add an item to the specific recipe.",
                            inline=False)
            embed.add_field(name="removeitem <Code name + item>", value="Remove an item from the specific recipe",
                            inline=False)
            embed.add_field(name="showrecipes", value="Shows all the recipes in the files.", inline=False)
            embed.add_field(name="showrecipe <Code name>", value="Shows a specific recipe and it's items", inline=False)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help_Messages(client))