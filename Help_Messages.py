import json
import random

import discord
from discord.ext import commands

import Discord_prof

import Company_Projects

import FFXIV

import Social

import Settings

Settings.init()
IDsDic = Settings.IDsDic


def SetEmbedCommands(emb, comm, commsList):
    emptyVal = "\u200b"
    numOfComms = len(commsList)

    indivlines = numOfComms // 3
    extralines = numOfComms % 3

    descs = {"desc0": "",
             "desc1": "",
             "desc2": ""
             }

    for i in range(0, 3):  # For every desc.
        for j in range(0, indivlines):  # For the amount of lines we need.
            descs["desc" + str(i)] += commsList[j*3 + i] + "\n"

    for i in range(0, extralines):  # For any extra line needed.
        descs["desc" + str(i)] += commsList[(numOfComms - extralines)]

    # Set empty values for the rest of desc if they dont have any value.
    for key in descs:
        if descs[key] == "":
            descs[key] = emptyVal

    # Set the fields.
    for i in range(0, 3):
        name = emptyVal
        if i == 0:
            name = comm
        emb.add_field(name=name, value=descs["desc" + str(i)], inline=True)

    return emb


class Help_Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help_message_compProjects(self, ctx):
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

    @commands.command()
    async def help(self, ctx, arg=None):
        embed = discord.Embed(title="**Commands**",
                              description="See all the commands here:",
                              color=Settings.generalColorEMB)
        embed.set_thumbnail(url=Settings.botIcon)
        # Add all the fields.
        embed = SetEmbedCommands(embed, "Profile", Discord_prof.Commands()[0])
        embed = SetEmbedCommands(embed, "Company projects", Company_Projects.Commands()[0])
        embed = SetEmbedCommands(embed, "FFXIV", FFXIV.Commands()[0])
        embed = SetEmbedCommands(embed, "Social", Social.Commands()[0])

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help_Messages(client))
