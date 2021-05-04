import discord

import requests

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

import json

import Settings

ffxivLodestoneIDPath = "Jsons_FFXIV/FFXIV_Lodestone_ID.json"

with open("Whoami_FFXIV/Whoami_User_Images.json") as file:
    UsersImgs = json.load(file)

# ** NOTE: General functions. ** #


async def GetUserLodestoneID(ctx, arg1, arg2, arg3, commandName):
    # Check if argument is a valid person, not a role or invalid.
    if arg1 is None or arg2 is None or arg3 is None:
        await ctx.send(embed=Settings.OnErrorMessage(commandName, 0))
        return False
    # Request from the api.
    urlInfo = requests.get("https://xivapi.com/character/search?name=" + arg1 + " " + arg2 + "&server=" + arg3)
    # Set the info to a dic.
    jsonInfo = json.loads(urlInfo.content)
    # If the char not found, send error.
    if not jsonInfo["Results"]:
        await ctx.send(embed=Settings.OnErrorMessage(commandName, 1))
        return False
    # Return the user's lodestone id.
    return str(jsonInfo["Results"][0]["ID"])


def CheckIfAuthorInfoChanged(author):
    with open(ffxivLodestoneIDPath) as f:
        Lodestone_IDDic = json.load(f)
    # Set the soup for every other info.
    requestResult = requests.get("https://na.finalfantasyxiv.com/lodestone/character/" + Lodestone_IDDic[author][0] + "/")
    soup = BeautifulSoup(requestResult.content, 'html.parser')

    titleNameWorld = TitleNameWorld(soup)

    nameSurname = titleNameWorld[1].split(' ')
    with open(ffxivLodestoneIDPath) as f:
        Lodestone_IDDic = json.load(f)
    with open(ffxivLodestoneIDPath, 'w') as file:
        id = Lodestone_IDDic[author][0]
        name = nameSurname[0]
        surname = nameSurname[1]
        world = titleNameWorld[2].split("\xa0")[0]
        Lodestone_IDDic.update({author: [id, name, surname, world]})
        file.write(json.dumps(Lodestone_IDDic, sort_keys=True, indent=4, separators=(',', ': ')))

# ** NOTE: Whoami functions. ** #


def GetTextPos(canvas, str, font, xPos):
    w, h = canvas.textsize(str, font=font)
    return (xPos - w) / 2


def MountMinionNum(charID):
    # Request from the site.
    reqResMoun = requests.get("https://na.finalfantasyxiv.com/lodestone/character/" + charID + "/mount/")
    # Get the soup parser.
    soupMoun = BeautifulSoup(reqResMoun.content, 'html.parser')
    # Get the info from the soup.
    soupResMoun = soupMoun.find('p', class_='minion__sort__total')
    # Get the mount number out of the soup result.
    mountNumber = soupResMoun.find("span").text

    # Request from the site.
    reqResMin = requests.get("https://na.finalfantasyxiv.com/lodestone/character/" + charID + "/minion/")
    # Get the soup parser.
    soupMin = BeautifulSoup(reqResMin.content, 'html.parser')
    # Get the info from the soup.
    soupResMin = soupMin.find('p', class_='minion__sort__total')
    # Get the minion number out of the soup result.
    minionNumber = soupResMin.find("span").text

    # Return both values.
    return mountNumber, minionNumber


def TitleNameWorld(soup):
    charTitle = soup.find(class_="frame__chara__title").text
    charName = soup.find(class_="frame__chara__name").text
    charWorld = soup.find(class_="frame__chara__world").text
    return charTitle, charName, charWorld


def CompanyCrest(soup):
    companyCrest = soup.find(class_="character__freecompany__crest__image").find_all('img')
    crest = Image.open(requests.get(companyCrest[0]['src'], stream=True).raw)
    # Paste the 3 images upon the first one.
    for i in range(1, 3):
        crest.paste(Image.open(requests.get(companyCrest[i]['src'], stream=True).raw),
                    (0, 0),
                    Image.open(requests.get(companyCrest[i]['src'], stream=True).raw))
    return crest


def RaceClan(soup):
    raceclan = soup.find(class_="character-block__name")
    newstr = str(raceclan.contents[2]).replace(' ', '')
    newstr = newstr[:-1].replace('/', '')
    return raceclan.contents[0]


def JobsDIC(soup):
    # Jobs and their level.
    jobsList = [
        ("Astrologian", ""),
        ("White Mage", "Conjurer"),
        ("Scholar", ""),
        ("Gunbreaker", ""),
        ("Dark Knight", ""),
        ("Warrior", "Marauder"),
        ("Paladin", "Gladiator"),
        ("Blue Mage", ""),
        ("Red Mage", ""),
        ("Black Mage", "Thaumaturge"),
        ("Summoner", "Arcanist"),
        ("Bard", "Archer"),
        ("Machinist", ""),
        ("Dancer", ""),
        ("Samurai", ""),
        ("Ninja", "Rogue"),
        ("Dragoon", "Lancer"),
        ("Monk", "Pugilist"),
        ("Alchemist", ""),
        ("Culinarian", ""),
        ("Weaver", ""),
        ("Leatherworker", ""),
        ("Carpenter", ""),
        ("Goldsmith", ""),
        ("Armorer", ""),
        ("Blacksmith", ""),
        ("Botanist", ""),
        ("Miner", ""),
        ("Fisher", "")
    ]
    # Get all the job info from the soup
    resURLS = soup.find_all('img', {'height': 24}, {'data-tooltip': True}, class_="js__tooltip")
    jobsDic = {}

    for i in resURLS:
        level = i.find_parent("li")
        # Change the blue mage text.
        if i['data-tooltip'] == 'Blue Mage (Limited Job)':
            jobsDic['Blue Mage'] = level.text  # , i['src'])
        else:
            jobsDic[i['data-tooltip'].split('/')[0].strip()] = level.text  # , i['src'])
    # Set for the jobs their lvl and name.
    for key in jobsDic:
        for ele in jobsList:
            if key in ele:
                tempList = list(ele)
                tempList[1] = jobsDic[key]
                jobsList[jobsList.index(ele)] = tuple(tempList)
    return jobsList


def AvatarIMG(soup):
    avatarWidHei = (450, 600)
    avatarSoup = soup.find('img', {'width': 220})
    return Image.open(requests.get(avatarSoup['src'], stream=True).raw).resize(avatarWidHei)


def BackgroundAvatarJobsIMG(avatarIMG, jobsList, backgroundImg, jobsImg, font, fontSize, charID):
    # Set the background size.
    backgroundWidHei = (900, 600)
    # Set the jobs position.
    jobsPos = (0, 0)
    # Set the avatar position.
    avatarPos = (0, 0)

    isAvatarNeeded = True
    # Open the background image.
    if charID in UsersImgs:
        background = Image.open(requests.get(UsersImgs[charID], stream=True).raw).resize(backgroundWidHei)
        isAvatarNeeded = False
    else:
        background = Image.open(backgroundImg, 'r').resize(backgroundWidHei)

    # Open the job image.
    jobs = Image.open(jobsImg, 'r')

    # Paste the images on the background.
    if isAvatarNeeded:
        background.paste(avatarIMG, avatarPos)
    background.paste(jobs, jobsPos, jobs)

    canvas = ImageDraw.Draw(background)
    font = ImageFont.truetype(font, size=fontSize)
    color = '#b2d2de'

    # Set the offset for every job.
    jobsOffSet = [
        (0, 0),
        (0.9, 0),
        (1.83, 0),
        (4, 0),
        (4.9, 0),
        (5.93, 0),
        (7, 0),
        (11, 0),
        (0, 1),
        (0.85, 1),
        (1.85, 1),
        (4, 1),
        (5, 1),
        (6, 1),
        (8, 1),
        (8.95, 1),
        (10, 1),
        (10.9, 1),
        (-0.1, 2),
        (0.9, 2),
        (2, 2),
        (3, 2),
        (4, 2),
        (4.95, 2),
        (5.95, 2),
        (6.9, 2),
        (9, 2),
        (10, 2),
        (11, 2)
    ]

    for i in range(0, len(jobsList)):
        jobsText = str(jobsList[i][1])

        offSetX = 465 + jobsOffSet[i][0] * 35
        offSetY = 445 + jobsOffSet[i][1] * 60

        if len(jobsText) < 2:
            offSetX += 4.45

        textOffset = (int(offSetX), int(offSetY))
        canvas.text(textOffset, jobsText, font=font, fill=color)

    return background


def BackTextMountMinionFCRC(background, font, fontSize, mountNum, minionNum, freeCompanyName, raceClan):
    canvas = ImageDraw.Draw(background)
    font = ImageFont.truetype(font, size=fontSize)
    color = (255, 255, 255)

    canvas.text((GetTextPos(canvas, "Free Company:", font, 1125), 155), "Free Company:", font=font, fill=color)
    canvas.text((GetTextPos(canvas, freeCompanyName, font, 1125), 195), freeCompanyName, font=font, fill=color)

    canvas.text((GetTextPos(canvas, "Race:", font, 1125), 275), "Race:", font=font, fill=color)
    canvas.text((GetTextPos(canvas, raceClan, font, 1125), 315), raceClan, font=font, fill=color)

    canvas.text((GetTextPos(canvas, "Mounts:", font, 1575), 155), "Mounts:", font=font, fill=color)
    canvas.text((GetTextPos(canvas, mountNum + "/198", font, 1575), 195), mountNum + "/189", font=font, fill=color)

    canvas.text((GetTextPos(canvas, "Minions:", font, 1575), 275), "Minions:", font=font, fill=color)
    canvas.text((GetTextPos(canvas, minionNum + "/407", font, 1575), 315), minionNum + "/392", font=font, fill=color)

    return background


def BackTextTitleNameWorld(background, font, fontSize, titleNameWorld):
    canvas = ImageDraw.Draw(background)
    font = ImageFont.truetype(font, size=fontSize)
    color = (255, 255, 255)

    canvas.text((GetTextPos(canvas, titleNameWorld[0], font, 1350), 10), titleNameWorld[0], font=font, fill=color)

    canvas.text((GetTextPos(canvas, titleNameWorld[1], font, 1350), 50), titleNameWorld[1], font=font, fill=color)

    canvas.text((GetTextPos(canvas, titleNameWorld[2], font, 1350), 90), titleNameWorld[2], font=font, fill=color)

    return background


def WhoamiImg(charID, backgroundImg, jobsImg, font):
    # Get the mount and minion number.
    mountNUM = MountMinionNum(charID)[0]
    minionNUM = MountMinionNum(charID)[1]

    # Set the soup for every other info.
    requestResult = requests.get("https://na.finalfantasyxiv.com/lodestone/character/" + charID + "/")
    soup = BeautifulSoup(requestResult.content, 'html.parser')

    # Get the free company name.
    freeCompanyName = soup.find_all(class_="character__freecompany__name")[0].find("a").text

    # Get the race and clan text.
    raceClan = RaceClan(soup)

    # Get the title, the name and the world of the player.
    titleNameWorld = TitleNameWorld(soup)

    # Get the avatar image.
    avatarImg = AvatarIMG(soup)

    # Get the job list.
    jobsList = JobsDIC(soup)

    # Set the images and texts on the background.
    background = BackgroundAvatarJobsIMG(avatarImg, jobsList, backgroundImg, jobsImg, font, 20, charID)
    background = BackTextMountMinionFCRC(background, font, 38, mountNUM, minionNUM, freeCompanyName, raceClan)
    return BackTextTitleNameWorld(background, font, 38, titleNameWorld)


# ** NOTE: Fflogs functions. ** #


def GetLinksInfo(user, world):
    # Get the image from the user's profile for the embed.
    requestResult = requests.get("https://www.fflogs.com/character/EU/" + world + "/" + user)
    soup = BeautifulSoup(requestResult.content, 'html.parser')
    avatarPic = soup.find(class_="character-name-link")

    # Check if the avatar is empty.
    if avatarPic is None:
        return False
    if not avatarPic.find_all('img'):
        return False

    # Get the image if found the user.
    avatarPic = avatarPic.find_all('img')[0]['src']

    # Get all the normal/savage info from the site.
    link = "https://www.fflogs.com:443/v1/parses/character/" + user + "/" + world + "/EU?metric=rdps&bracket=0&partition=1&timeframe=historical&includeCombatantInfo=false&api_key=703d7039a0d96ac208edc4f82aded59b"

    urlInfo = requests.get(link)
    jsonInfo = json.loads(urlInfo.content)

    # Return both values.
    return avatarPic, jsonInfo


def GetFflogsInfo(info, diff):
    # Set the dictionary to change the names in the end.
    fightNames = {
        "73": "Cloud of darkness",
        "74": "Shadowkeeper",
        "75": "Fatebreaker",
        "76": "Eden's Promise",
        "77": "Oracle of Darkness"
    }
    # Set the empty dic for the information.
    fight = {}
    # Fill the dictionary with empty values.
    for i in range(0, 5):
        fight[str(73 + i)] = [-1, 0, "", 0]  # 1st parse, 2nd damage, 3rd job, 4th kills.

    for i in range(0, len(info)):
        # Check if the info's diff is the same as asked.
        if info[i]["difficulty"] == diff:
            for j in range(0, 5):
                fightID = 73 + j
                # Check which fight it got from the site info.
                if info[i]["encounterID"] == fightID:
                    # If found increase the kills.
                    fight[str(fightID)][3] += 1
                    # If the parse seen is higher from the old one change the values.
                    if info[i]["percentile"] > fight[str(fightID)][0]:
                        fight[str(fightID)][0] = info[i]["percentile"]
                        fight[str(fightID)][1] = info[i]["total"]
                        fight[str(fightID)][2] = info[i]["spec"]

    # Create a new dictionary to replace the values to the fight names.
    newDic = {}
    for key in fight:
        newDic[fightNames[key]] = fight[key]

    return newDic


async def SendLogs(ctx, user, world):
    # Get the results from the fflogs site.
    returns = GetLinksInfo(user, world)
    # If the user was not found return an error message.
    if returns is False:
        embed = discord.Embed(title="Y'shtola found an issue.",
                              description="I cound not find your character in the fflogs site.",
                              color=Settings.generalColorEMB)

        embed.set_thumbnail(url=Settings.botIcon)
        await ctx.send(embed=embed)
        return

    areSavageLogs = "savage"
    # Get the dictionary fight savage first.
    fightDic = GetFflogsInfo(returns[1], 101)
    emptyParses = 0

    # Check if the savage logs are empty.
    for key in fightDic:
        if fightDic[key][0] == -1:
            emptyParses += 1

    # If the savage logs are empty, get the normal logs.
    if emptyParses == 5:
        fightDic = GetFflogsInfo(returns[1], 100)
        areSavageLogs = "normal"

    link = "https://www.fflogs.com/character/EU/" + world + "/" + user.replace(" ", "%20")

    embed = discord.Embed(title=user,
                          description="**Eden's promise " + areSavageLogs + "**",
                          colour=Settings.generalColorEMB,
                          url=link
                          )
    embed.set_thumbnail(url=returns[0])

    for key in fightDic:
        if fightDic[key][0] != -1:
            dps = str(int(fightDic[key][1]))
            job = str(fightDic[key][2])
            perc = str(int(fightDic[key][0]))
            kills = str(fightDic[key][3])
            message = dps + " dps as " + job + " " + perc + "% with " + kills + " kills."
            embed.add_field(name=key, value=message, inline=False)

    return embed
