import discord
from discord.ext import commands
from discord import app_commands

from bert import BertBot

class GearCog(commands.Cog):

    bert : "BertBot"

    def __init__(self, client : "BertBot") -> None:

        self.client = client

    