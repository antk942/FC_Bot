import discord

import Settings


async def FCSchedule(ctx):
    embed = discord.Embed(title="SCHEDULE",
                          description="**Monday:**\n```bash\n\"Free or Savage runs\"```\n"
                                      "**Tuesday:**\n```bash\n\"Free\"```\n"
                                      "**Wednesday:**\nOrganizer: <@176301875920896000>\n```bash\n\"Treasure Maps\" - 16:00 or 18:00 ST```\n"
                                      "**Thursday:**\n```bash\n\"Free\"```\n"
                                      "**Friday:**\nOrganizer: <@327572759431610368>\n```bash\n\"Legacy raids\" - 16:00 or 18:00 ST```\n"
                                      "**Saturday:**\nOrganizer: Flexible\n```bash\n\"Extreme mount farms\"```\n"
                                      "**Sunday:**\n```bash\n\"Free or Savage runs\"```\n",
                          color=Settings.generalColorEMB)

    embed.set_footer(text="If you have any questions regarding a specific event, "
                          "please contact the person/people leading that event, "
                          "failing that, feel free to also contact our leader.",
                     icon_url=Settings.botIcon)

    embed.set_thumbnail(url=Settings.botIcon)
    await ctx.send(embed=embed)


async def TrialsARR(ctx):
    trials = {
        "Garuda": "The Howling Eye <:Garuda:863353191055753276>",
        "Titan": "The Navel <:Titan:863353191609270272>",
        "Ifrit": "The Bowl of Embers <:Ifrit:863353191290372106>",
        "Leviathan": "The Whorleater <:Leviathan:863353191075938335>",
        "Ramuh": "The Striking Tree <:Ramuh:863353191374913536>",
        "Shiva": "Akh Afah Amphitheatre <:Shiva:863353191348830219>",
        "Nightmare": "Garuda Titan Ifrit <:Nightmare:863353191151960075>"

    }
    emojis = [
        "<:Garuda:863353191055753276>",
        "<:Titan:863353191609270272>",
        "<:Ifrit:863353191290372106>",
        "<:Leviathan:863353191075938335>",
        "<:Ramuh:863353191374913536>",
        "<:Shiva:863353191348830219>",
        "<:Nightmare:863353191151960075>"
    ]
    embed = discord.Embed(title="A Realm Reborn.",
                          description="***Horses***",
                          color=Settings.generalColorEMB)
    for key in trials:
        embed.add_field(name=key, value=trials[key], inline=False)

    embed.set_thumbnail(url=Settings.ARRIcon)
    message = await ctx.send(embed=embed)
    for item in emojis:
        await message.add_reaction(item)


async def TrialsHW(ctx):
    trials = {
        "Bismarck": "The Limitless Blue <:Bismarck:863353434878771230>",
        "Ravana": "Thok ast Thok <:Ravana:863353435176828958>",
        "King Thordan": "The Minstrel's Ballad: Thordan's Reign <:Thordan:863353435814494248>",
        "Nidhogg": "The Minstrel's Ballad: Nidhogg's Rage <:Nidhogg:863353434991886346>",
        "Sephirot": "Containment Bay S1T7 <:Sephirot:863353435104215041>",
        "Sophia": "Containment Bay P1T6 <:Sophia:863353435880685568>",
        "Zurvan": "Containment Bay Z1T9 <:Zurvan:863353435851194378>"

    }
    emojis = [
        "<:Bismarck:863353434878771230>",
        "<:Ravana:863353435176828958>",
        "<:Thordan:863353435814494248>",
        "<:Nidhogg:863353434991886346>",
        "<:Sephirot:863353435104215041>",
        "<:Sophia:863353435880685568>",
        "<:Zurvan:863353435851194378>"
    ]
    embed = discord.Embed(title="Heavensward.",
                          description="***Birds***",
                          color=Settings.generalColorEMB)
    for key in trials:
        embed.add_field(name=key, value=trials[key], inline=False)

    embed.set_thumbnail(url=Settings.HWIcon)
    message = await ctx.send(embed=embed)
    for item in emojis:
        await message.add_reaction(item)


async def TrialsSB(ctx):
    trials = {
        "Lakshmi": "Emanation <:Lakshmi:863353469146497065>",
        "Susano": "The Pool of Tribute <:Susano:863353469539975178>",
        "Shinryu": "The Minstrel's Ballad: Shinryu's Domain <:Shinryu:863353469431709706>",
        "Byakko": "The Jade Stoa <:Byakko:863353469221470258>",
        "Tsukuyomi": "The Minstrel's Ballad: Tsukuyomi's Pain <:Tsukuyomi:863353469615734815>",
        "Suzaku": "Hells' Kier <:Suzaku:863353469619929128>",
        "Seiryu": "The Wreath of Snakes <:Seiryu:863353469075324939>"

    }
    emojis = [
        "<:Lakshmi:863353469146497065>",
        "<:Susano:863353469539975178>",
        "<:Shinryu:863353469431709706>",
        "<:Byakko:863353469221470258>",
        "<:Tsukuyomi:863353469615734815>",
        "<:Suzaku:863353469619929128>",
        "<:Seiryu:863353469075324939>"
    ]
    embed = discord.Embed(title="Stormblood.",
                          description="***Wolfs***",
                          color=Settings.generalColorEMB)
    for key in trials:
        embed.add_field(name=key, value=trials[key], inline=False)

    embed.set_thumbnail(url=Settings.SBIcon)
    message = await ctx.send(embed=embed)
    for item in emojis:
        await message.add_reaction(item)


async def TrialsShB(ctx):
    trials = {
        "Titania": "The Dancing Plague <:Titania:863391802765606922>",
        "Innocence": "The Crown of the Immaculate <:Innocence:863391802765606932>",
        "Hades": "Minstrel's Ballad: Hade's Elegy <:Hades:863391802109984789>",
        "Ruby Weapon": "Cinder Drift <:RubyWeapon:863391802508705803>",
        "Warrior of Light": "The Seat of Sacrifice <:SeatOfSacrifice:863391802823016458>",
        "The Emerald Weapon": "Castrum Marinum <:EmeraldWeapon:863391802380124200>",
        "The Diamond Weapon": "The Cloud Deck <:DiamondWeapon:863391801921634314>"

    }
    emojis = [
        "<:Titania:863391802765606922>",
        "<:Innocence:863391802765606932>",
        "<:Hades:863391802109984789>",
        "<:RubyWeapon:863391802508705803>",
        "<:SeatOfSacrifice:863391802823016458>",
        "<:EmeraldWeapon:863391802380124200>",
        "<:DiamondWeapon:863391801921634314>"
    ]
    embed = discord.Embed(title="Shadowbringer.",
                          description="***Dragons***",
                          color=Settings.generalColorEMB)
    for key in trials:
        embed.add_field(name=key, value=trials[key], inline=False)

    embed.set_thumbnail(url=Settings.ShBIcon)
    message = await ctx.send(embed=embed)
    for item in emojis:
        await message.add_reaction(item)


async def SavageRaids(ctx):
    raids = {
        "Gobwalker": "The Burden of the Father 🚙",
        "Arrhidaeus": "The Soul of the Creator 🤖",
        "Alte Roite": "Deltascape V4.0 🐍",
        "Air Force": "Sigmascape V4.0 ✈️",
        "Omega": "Alphascape V4.0 🕷️",
        "Skyslipper": "Eden Gate: Sepulture 🌎",
        "Ramuh": "Eden Verse: Refulgance 🧊"

    }
    emojis = [
        "🚙",
        "🤖",
        "🐍",
        "✈️",
        "🕷️",
        "🌎",
        "🧊"
    ]
    embed = discord.Embed(title="Savage raids.",
                          description="***Legacy mounts***",
                          color=Settings.generalColorEMB)
    for key in raids:
        embed.add_field(name=key, value=raids[key], inline=False)

    embed.set_thumbnail(url=Settings.botIcon)
    message = await ctx.send(embed=embed)
    for item in emojis:
        await message.add_reaction(item)


async def SendDMOnServerJoin(member):
    emb = discord.Embed(title="Welcome to Phantoms of Glory.",
                        description="Hello, before you start your adventure you should check out some things.",
                        color=Settings.generalColorEMB)
    emb.add_field(name="Rules.", value="Make sure you read carefully our rules.\n"
                                       "[Rules](https://discord.com/channels/824112000342032385/824123037028188160/824488287976161320)",
                  inline=False)
    emb.add_field(name="Assign roles.", value="Check out all the cool roles you can have.\n"
                                              "[Assign roles](https://discord.com/channels/824112000342032385/841952676317233182/841955569153998888)",
                  inline=False)
    emb.add_field(name="Events.", value="There you will find about all the nice events we organize.\n"
                                        "Some of them being mount farms glamour competition etc.", inline=False)
    emb.add_field(name="Mount farms.", value="Extreme trials mounts:\n"
                                             "[Extremes](https://discord.com/channels/824112000342032385/830135464526610532/863706056637808671)\n"
                                             "Legacy mounts:\n"
                                             "[Legacy](https://discord.com/channels/824112000342032385/855136480120143912/863706006176399390)")
    emb.set_footer(text="Make sure if you have any questions to contact any council member.",
                   icon_url=Settings.botIcon)
    await member.send(embed=emb)