import discord
from discord.ext import commands

import Discord_prof
from Discord_prof import Discord_prof

from FFXIV import FFXIV

from Company_Projects import Company_Projects

from Social import Social

from Event import Event

from Help_Messages import Help_Messages

import FFXIV_Announcements

import Settings

import ctypes.util

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

# Add cogs.
bot.add_cog(Discord_prof(bot))
bot.add_cog(FFXIV(bot))
bot.add_cog(Company_Projects(bot))
bot.add_cog(Social(bot))
bot.add_cog(Event(bot))
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
    
    # Check the author.
    if Settings.ChangeAuthorID(ctx) != IDsDic["Kon"]:
        return

    channel = 836525085224730654
    title = "*Mother's day special.*"
    url = "https://cdn.discordapp.com/attachments/837628182244622337/839100220100968468/panda.png"
    description = "As a mother of our lovely FC, Kon will give everyone a special apple juice with a chicken for dinner.\n" \
                  "If you want stop by the entrance " + regEm["g_love"]

    picture = "https://cdn.discordapp.com/attachments/837628182244622337/840896937486057502/Screenshot_83.png"

    # Set the embed details.
    newEmbd = discord.Embed(title=title, url=url, description=description, color=Settings.generalColorEMB)
    # Set the embed url.
    newEmbd.set_image(url=picture)
    # Set the bot icon.
    # newEmbd.set_thumbnail(url=Settings.botIcon)
    # Set footer text.
    #newEmbd.set_footer(text="Click the title link.")

    await bot.get_channel(channel).send("@everyone")
    await bot.get_channel(channel).send(embed=newEmbd)


@bot.event
async def on_ready():
    print('bot ready')
    # await bot.get_channel(824436047593209858).send("bot is online")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="me being the best"))









































# token
bot.run('ODI0NDMyOTk1ODUwNzgwNzEy.YFvTDw.jDa5Bmcicrs2fx8QooLKSRuTqbc')
# end of token
