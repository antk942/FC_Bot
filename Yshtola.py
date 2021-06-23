import discord
from discord.ext import commands, tasks

import Discord_prof
from Discord_prof import Discord_prof

from FFXIV import FFXIV

from Company_Projects import Company_Projects

from Social import Social

from Event import Event

from Reaction_Role import Reaction_Role

from Help_Messages import Help_Messages

import FFXIV_Announcements

import Settings

import ctypes.util

import time

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

# Add cogs.
bot.add_cog(Discord_prof(bot))
bot.add_cog(FFXIV(bot))
bot.add_cog(Company_Projects(bot))
bot.add_cog(Social(bot))
bot.add_cog(Event(bot))
bot.add_cog(Reaction_Role(bot))
bot.add_cog(Help_Messages(bot))

# Settings initialization.
Settings.init()

regEm = Settings.RegEmojDic
animEm = Settings.AnimatedEmojDic

IDsDic = Settings.IDsDic


# region Heroku magic
print("ctypes - Find opus:")
a = ctypes.util.find_library('opus')
print(a)

print("Discord - Load Opus:")
b = discord.opus.load_opus(a)
print(b)

print("Discord - Is loaded:")
c = discord.opus.is_loaded()
print(c)
# endregion


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
    # Json data download.
    await Discord_prof.GiveData(bot, message)

    await bot.process_commands(message)


@bot.command()
async def megalazer(ctx):
    sendMes = ""
    for i in range(1, 10):
        sendMes += animEm["MegaLazer" + str(i)]
        if i % 3 == 0:
            sendMes += "\n"
    await ctx.message.delete()
    await ctx.send(sendMes)


@bot.command()
async def sendTempEMB(ctx):
    await ctx.message.delete()
    channel = bot.get_channel(824706330237075476)
    embed = discord.Embed(title="SCHEDULE",
                          description="**Monday:**\n```bash\n\"Free\"```\n"
                                      "**Tuesday:**\n```bash\n\"Reclear\"```\n"
                                      "**Wednesday:**\nOrganizer: <@176301875920896000>/<@429720174913126401>\n```bash\n\"Treasure Maps\" - 16:00 ST```\n"
                                      "**Tuesday:**\nOrganizer: <@327572759431610368>\n```bash\n\"Legacy Raids\" - 15:00 ST```\n"
                                      "**Friday:**\nOrganizer: <@356385267545800704>\n```bash\n\"Extreme Mount Farming\" - 16:00 ST```\n"
                                      "**Saturday:**\n```bash\n\"Alliance Raids\"```\n"
                                      "**Sunday:**\nOrganizer: <@356385267545800704>\n```bash\n\"Unreal\" - 17:00 ST```\n",
                          color=Settings.generalColorEMB)

    embed.set_footer(text="If you have any questions regarding a specific event, "
                          "please contact the person/people leading that event, "
                          "failing that, feel free to also contact our majestic leader.",
                     icon_url=Settings.botIcon)

    embed.set_thumbnail(url=Settings.botIcon)
    await ctx.send(embed=embed)


@tasks.loop(seconds=30.0)
async def ShowGMTPresence():
    now = "ST is: " + time.strftime("%H:%M", time.gmtime())
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=now))


@bot.event
async def on_ready():
    print('bot ready')
    #await bot.get_channel(824436047593209858).send(IDsDic["Kon"])
    await bot.wait_until_ready()
    ShowGMTPresence.start()









































# token
bot.run('ODI0NDMyOTk1ODUwNzgwNzEy.YFvTDw.jDa5Bmcicrs2fx8QooLKSRuTqbc')
# end of token
