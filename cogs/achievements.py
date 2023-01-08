import discord
from discord import app_commands
from discord.ext import commands
from objects.achievements.AchievementManager import AchievementManager

from bert import BertBot

class AchievementsCog(commands.Cog):

    client : BertBot
    achieveman : AchievementManager

    def __init__(self, client : "BertBot") -> None:
        self.client = client

        self.achieveman = self.client.achieveman

    @app_commands.command(
        name = "achievements",
        description = "View a list of your achievements"
    )
    async def achievements_achievements(
        self, interaction : discord.Interaction
    ) -> None:
        return await interaction.response.send_message(
            "Not Implemented", ephemeral = True
        )

async def setup(client):
    await client.add_cog(AchievementsCog(client))