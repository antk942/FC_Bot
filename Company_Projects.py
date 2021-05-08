import json
from time import strftime

import discord
from discord.ext import commands

import Settings

Settings.init()
companyRegEm = Settings.RegEmojDic
companyAnimEm = Settings.AnimatedEmojDic

# Json paths.
recipesPath = "Jsons_Company/Recipes.json"
recipeItemsPath = "Jsons_Company/RecipeItems.json"

# Open jsons.
with open(recipesPath) as f:
    RecipesDic = json.load(f)
with open(recipeItemsPath) as f:
    RecipeItemsDic = json.load(f)


def Commands():
    commList = ["addrecipe",
                "clearrecipe",
                "additem",
                "removeitem",
                "showrecipes",
                "showrecipe"]
    commsExplanation = ["Give a love to someone.",
                        "Get your daily chips.",
                        "Give chips to someone.",
                        "Check out your profile information.",
                        "See who has the most love.",
                        "See who has the most chips."]

    return commList, commsExplanation


class Company_Projects(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addrecipe(self, ctx, *arg):
        # Take the arg into a str.
        recipe = ' '.join(arg)

        # See if the recipe is in the json.
        if recipe in RecipesDic:
            await ctx.send(ctx.author.mention + " this recipe is already in my files. " + companyRegEm["g_wee"])
            return

        # Make the codename based on the first 3 letters of the recipe and the time.
        codeName = recipe[0] + recipe[1] + recipe[2] + strftime("%a%b%H%M")

        # Write on the recipe json.
        with open(recipesPath, 'w') as file:
            RecipesDic.update({codeName: recipe})
            file.write(json.dumps(RecipesDic, sort_keys=True, indent=4, separators=(',', ': ')))

        # Write on the recipe items json.
        with open(recipeItemsPath, 'w') as file:
            RecipeItemsDic.update({codeName: ""})
            file.write(json.dumps(RecipeItemsDic, sort_keys=True, indent=4, separators=(',', ': ')))
        await ctx.send(
            ctx.author.mention + " i successfully saved your recipe with the code name: " + codeName + " " + companyRegEm[
                "g_vibe"])

    @commands.command()
    async def clearrecipe(self, ctx, arg):
        if not RecipesDic:
            await ctx.send(ctx.author.mention + " there are no recipes to delete. " + companyRegEm["g_shock"])
            return

        # Delete all recipes depending on the arg.
        if arg == "all":
            # From the recipe json.
            with open(recipesPath, 'w') as file:
                RecipesDic.clear()
                json.dump({}, file)

            # From the recipe items json.
            with open(recipeItemsPath, 'w') as file:
                RecipeItemsDic.clear()
                json.dump({}, file)
            await ctx.send(ctx.author.mention + " i cleared all the recipes. " + companyRegEm["g_shock"])
            return

        # See if the recipe the author asked is in the jsons.
        if arg not in RecipesDic:
            await ctx.send(ctx.author.mention + " this recipe does not exist.")
            return

        # From the recipe json.
        with open(recipesPath, 'w') as file:
            del RecipesDic[arg]
            file.write(json.dumps(RecipesDic, sort_keys=True, indent=4, separators=(',', ': ')))

        # From the recipe items json.
        with open(recipeItemsPath, 'w') as file:
            del RecipeItemsDic[arg]
            file.write(json.dumps(RecipeItemsDic, sort_keys=True, indent=4, separators=(',', ': ')))

        await ctx.send(ctx.author.mention + " i cleared the recipe you wanted. " + companyRegEm["g_shock"])

    @commands.command()
    async def additem(self, ctx, *arg):
        recipeName = arg[0]
        if recipeName not in RecipesDic:
            await ctx.send(ctx.author.mention + " i could not find this recipe " + companyRegEm["g_shock"])
            return

        # Create a list of the item.
        argList = list(arg)
        del argList[0]
        endSTR = ""
        for i in range(0, len(argList)):
            endSTR += argList[i] + ' '
        item = endSTR[:-1]

        # If the recipe items with that recipe is empty create the list and update the json with it.
        if RecipeItemsDic[recipeName] == "":
            with open(recipeItemsPath, 'w') as file:
                itemsList = [item]
                RecipeItemsDic.update({recipeName: itemsList})
                file.write(json.dumps(RecipeItemsDic, sort_keys=True, indent=4, separators=(',', ': ')))
                await ctx.send(ctx.author.mention + " added " + item + " to the recipe " + recipeName)
            return

        # Change the list of the json to tuple then to list update the list and update the json.
        itemsTuple = tuple(RecipeItemsDic[recipeName])
        itemsList = list(itemsTuple)
        itemsList.append(item)
        with open(recipeItemsPath, 'w') as file:
            RecipeItemsDic[recipeName] = itemsList
            file.write(json.dumps(RecipeItemsDic, sort_keys=True, indent=4, separators=(',', ': ')))

        await ctx.send(ctx.author.mention + " added " + item + " to the recipe " + recipeName)

    @commands.command()
    async def removeitem(self, ctx, *arg):

        recipeName = arg[0]
        if recipeName not in RecipesDic:
            await ctx.send(ctx.author.mention + " i could not find this recipe " + companyRegEm["g_shock"])
            return

        # Make the args to a list remove the first one, is the recipe, remove the last char, is a space.
        argList = list(arg)
        del argList[0]
        endSTR = ""
        for i in range(0, len(argList)):
            endSTR += argList[i] + ' '
        item = endSTR[:-1]

        # If the item does not exist return.
        if item not in RecipeItemsDic[recipeName]:
            await ctx.send(ctx.author.mention + " i could not find this item " + companyRegEm["g_shock"])
            return

        # Make the list from the json into a tuple then to a list remove the item.
        itemsTuple = tuple(RecipeItemsDic[recipeName])
        itemsList = list(itemsTuple)
        itemsList.remove(item)

        # Update the json.
        with open(recipeItemsPath, 'w') as file:
            RecipeItemsDic[recipeName] = itemsList
            file.write(json.dumps(RecipeItemsDic, sort_keys=True, indent=4, separators=(',', ': ')))

        await ctx.send(ctx.author.mention + " removed " + item + " from the recipe " + recipeName)

    @commands.command()
    async def showrecipes(self, ctx):

        if not RecipesDic:
            await ctx.send(ctx.author.mention + " i am sorry i have no recipes saved. " + companyRegEm["g_cry"])
            return
        allRecipes = ''

        # Get the recipes with the code names into a string.
        for key in RecipesDic:
            allRecipes += "**Code name:** " + key + "\t**Recipe:** " + RecipesDic[key] + '\n'
        itemsEmbed = discord.Embed(title="Recipes",
                                   description=allRecipes,
                                   color=Settings.generalColorEMB)
        itemsEmbed.set_thumbnail(url=Settings.botIcon)

        await ctx.send(embed=itemsEmbed)

    @commands.command()
    async def showrecipe(self, ctx, arg=None):

        if arg is None:
            Settings.OnErrorMessage("showrecipes", 0)
        if arg not in RecipesDic:
            await ctx.send(ctx.author.mention + " there is no recipe with this name " + companyRegEm["g_cry"])
            return
        items = ""
        itemsTuple = tuple(RecipeItemsDic[arg])
        itemsList = list(itemsTuple)

        # Save the items to a string.
        for ele in itemsList:
            items += ele + "\n"
        itemsEmbed = discord.Embed(title=RecipesDic[arg],
                                   description=items,
                                   color=Settings.generalColorEMB)
        itemsEmbed.set_thumbnail(url=Settings.botIcon)

        await ctx.send(embed=itemsEmbed)


def setup(client):
    client.add_cog(Company_Projects(client))
