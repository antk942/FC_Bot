import json

import random

import discord
from discord.ext import commands

import Settings

Settings.init()


class FFXIV_Announcements(commands.Cog):
    def __init__(self, client):
        self.client = client




def setup(client):
    client.add_cog(FFXIV_Announcements(client))