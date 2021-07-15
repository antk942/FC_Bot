import json
import random

import discord
from discord.ext import commands

import Discord_prof

import Company_Projects

import FFXIV

import Social

import Administration

import Settings

Settings.init()
IDsDic = Settings.IDsDic


def AddFieldsToHelp(emb, comm, commsList):
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
            descs["desc" + str(i)] += commsList[j * 3 + i] + "\n"

    for i in range(0, extralines):  # For any extra line needed.
        descs["desc" + str(i)] += commsList[(numOfComms - extralines + i)]

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


async def SendAllCommands(ctx, categories):
    embed = discord.Embed(title="**Commands**",
                          description="See all the commands here:",
                          color=Settings.generalColorEMB)

    # Add all the fields.
    for key in categories:
        embed = AddFieldsToHelp(embed, key, categories[key][0])

    embed.set_footer(text="For more information on a command try $help <command name>,\n "
                          "or on a category <category name>",
                     icon_url=Settings.botIcon)

    await ctx.send(embed=embed)


async def SendCommandsInCategory(ctx, categories, givenArg):
    embed = discord.Embed(title="**" + givenArg + " commands**",
                          description=ctx.author.mention,
                          color=Settings.generalColorEMB)
    # Add the field.
    explanations = categories[givenArg][1]
    for key in explanations:
        embed.add_field(name=key, value=explanations[key][0], inline=False)
    await ctx.send(embed=embed)


async def SendSpecificCommand(ctx, categories, givenArg, key, commKey):
    embed = discord.Embed(title="**" + givenArg + " explanation**",
                          description=ctx.author.mention,
                          color=Settings.generalColorEMB)
    embed.add_field(name=categories[key][1][commKey][0],
                    value=categories[key][1][commKey][1],
                    inline=False)
    await ctx.send(embed=embed)


class Help_Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *arg):
        categories = {
            "Profile": [Discord_prof.Commands()[0],
                        Discord_prof.Commands()[1]],
            "Company projects": [Company_Projects.Commands()[0],
                                 Company_Projects.Commands()[1]],
            "FFXIV": [FFXIV.Commands()[0],
                      FFXIV.Commands()[1]],
            "Social": [Social.Commands()[0],
                       Social.Commands()[1]]
        }
        specialCategories = {
            "Admins": [Administration.Commands()[0],
                       Administration.Commands()[1]]
        }

        # Take the arg into a str.
        givenArg = ' '.join(arg)

        if not givenArg:
            await SendAllCommands(ctx, categories)
            return

        # Send an explanation for a category.
        if givenArg in categories:
            await SendCommandsInCategory(ctx, categories, givenArg)
            return
        elif givenArg in specialCategories:
            author = Settings.RemoveExclaFromID(ctx.author.mention)
            if not ctx.author.guild_permissions.administrator or author not in Settings.admins:
                return
            await SendCommandsInCategory(ctx, specialCategories, givenArg)
            return

        # Send information on how to use a command.
        for key in categories:
            for commKey in categories[key][1]:
                if commKey == givenArg:
                    await SendSpecificCommand(ctx, categories, givenArg, key, commKey)
                    return

        await ctx.send(ctx.author.mention + " the argument you provided is not valid. Make sure you typed correctly.")


def setup(bot):
    bot.add_cog(Help_Messages(bot))
