import discord
from discord.ext import commands, tasks

import json

from Discord_prof import Discord_prof

from FFXIV import FFXIV

from Company_Projects import Company_Projects

from Social import Social

from CreateEvent import CreateEvent

from Reactions_Handler import Reactions_Handler

from Help_Messages import Help_Messages

from Administration import Administration

import FFXIV_Announcements

import TemporaryEmbedMessages

import Settings

import ctypes.util

import time

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

# Add cogs.
bot.add_cog(Discord_prof(bot))
bot.add_cog(FFXIV(bot))
bot.add_cog(Company_Projects(bot))
bot.add_cog(Social(bot))
bot.add_cog(CreateEvent(bot))
bot.add_cog(Administration(bot))
bot.add_cog(Reactions_Handler(bot))
bot.add_cog(Help_Messages(bot))

# Settings initialization.
Settings.init()

regEm = Settings.RegEmojDic
animEm = Settings.AnimatedEmojDic

IDsDic = Settings.IDsDic


@bot.event
async def on_message(message):
    # Fashion report.
    await FFXIV_Announcements.FashionReport(bot, message)
    # Weekly Reset.
    await FFXIV_Announcements.WeeklyReset(bot, message)
    # Weekly cackpot.
    await FFXIV_Announcements.Cackpot(bot, message)
    # Ffxiv lodestone announcements.
    await FFXIV_Announcements.Ffxiv_Lodestone(bot, message)

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    if member.guild.id == 824112000342032385:
        try:
            role = discord.utils.get(member.guild.roles, name="Wisp")
            await member.add_roles(role)
        except:
            await bot.get_channel(824436047593209858).send("Could not give role for some reason, investigate")
        try:
            await TemporaryEmbedMessages.SendDMOnServerJoin(member)
        except:
            await bot.get_channel(824436047593209858).send("Could not send message to the new guy, investigate")


@bot.command()
async def sendTempEMB(ctx, arg):
    #await ctx.message.delete()
    author = Settings.RemoveExclaFromID(ctx.author.mention)
    if author != IDsDic["Kon"]:
        return

    # Schedule.
    if arg == "Schedule":
        await TemporaryEmbedMessages.FCSchedule(ctx)
    # Extreme trials.
    elif arg == "Extreme":
        await TemporaryEmbedMessages.TrialsARR(ctx)
        await TemporaryEmbedMessages.TrialsHW(ctx)
        await TemporaryEmbedMessages.TrialsSB(ctx)
        await TemporaryEmbedMessages.TrialsShB(ctx)
    # Savage raids.
    elif arg == "Savage":
        await TemporaryEmbedMessages.SavageRaids(ctx)
    # On join message.
    elif arg == "DMOnJoin":
        guild = discord.utils.find(lambda g: g.id == ctx.guild.id, bot.guilds)
        member = await guild.fetch_member(str(ctx.author.id))
        await TemporaryEmbedMessages.SendDMOnServerJoin(member)


@tasks.loop(seconds=30.0)
async def ShowGMTPresence():
    now = "ST is: " + time.strftime("%H:%M", time.gmtime())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=now))


@tasks.loop(seconds=360.0)
async def DailyRefreshes():
    timeN = time.strftime("%H:%M", time.gmtime())
    check = timeN.split(":")
    if check[0] == "01":
        await Discord_prof.DailyREF(bot)
        marketBoardChannel = 858749666765570058
        for i in range(0, 10):
            await Settings.PurgeMessages(bot, marketBoardChannel, 100)


@bot.event
async def on_ready():
    print('bot ready')
    # await bot.get_channel(824436047593209858).send(IDsDic["Kon"])
    await bot.wait_until_ready()
    ShowGMTPresence.start()
    DailyRefreshes.start()


# token
bot.run('Bot_Token')
# end of token
