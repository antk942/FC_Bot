from discord.ext import commands

import Settings

Settings.init()
IDsDic = Settings.IDsDic
regEmoj = Settings.RegEmojDic


def Commands():
    commList = [
        "clear"
    ]

    commsExplanation = {
        "clear": ["Clear an amount of messages, default 5, available only to The Top Guy.",
                  "$clear <amount>/ optional"]
    }

    return commList, commsExplanation


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.message.delete()
        # Change the author id.
        author = Settings.RemoveExclaFromID(ctx.author.mention)

        if author != IDsDic["Shiroi"] and author != IDsDic["Kon"] and author != IDsDic["Lili"] and author != IDsDic["Mid"]:
            return

        await Settings.PurgeMessages(self.bot, ctx.channel.id, amount)



def setup(bot):
    bot.add_cog(Administration(bot))
