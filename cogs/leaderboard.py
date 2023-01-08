import discord
from discord.ext import commands
from discord import app_commands

from bert import BertBot

class LeaderboardCog(commands.GroupCog, name="leaderboard"):

    client : BertBot

    def __init__(self, client : "BertBot") -> None:
        self.client = client
        super().__init__()

    @app_commands.command(
        name = "money",
        description = "Display the leaderboard for who has the most money"
    )
    async def leaderboard_money(self, interaction : discord.Interaction) -> None:
        lb = await self.client.ecoman.get_leaderboard()
        lb = list(
            filter(
                lambda u: u[0] in [m.id for m in interaction.guild.members], lb
            )
        )

        dabloons_emoji = self.client.emoji_map.fetch_first("DABLOONS")

        leaderboard_text = "\n".join(
            [
                f"**{i}.** <@{m[0]}> - **{m[1]:,}** {dabloons_emoji}" for i, m in enumerate(lb[:10], start=1)
            ]
        )
        return await interaction.response.send_message(
            embed = discord.Embed(
                description = leaderboard_text
            ).set_author(
                name = "Top %d richest users in %s" % (len(leaderboard_text.split('\n')), interaction.guild.name),
                icon_url = interaction.guild.icon
            )
        )

async def setup(client):
    await client.add_cog(
        LeaderboardCog(client)
    )