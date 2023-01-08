from discord.ext import commands
from discord import app_commands
import discord

class TestCog(commands.Cog):
    
    def __init__(self, client : commands.Bot) -> None:
        self.client = client

    @app_commands.command(
        name = "ping",
        description="Test to see if Bert is alive",
    )
    async def test_ping(self, interaction : discord.Interaction):
        await interaction.response.send_message(
            "🧀 Pong!",
            ephemeral = True
        )

async def setup(client : commands.Bot):
    await client.add_cog(
        TestCog(client)
    )