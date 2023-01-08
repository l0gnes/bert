from discord.ext import commands
from discord import app_commands
import discord
from datetime import datetime
from objects.explosion.ExplosionReason import ExplosionReason
from typing import Union

# Weather API Key: c178dc07b1fd4aee9a2222918221412

class CheeseCog(commands.Cog):

    last_fed_by : discord.User

    weather_location_postal_codes = (
        "B4P2P2",
        "B4N5J5",
        "B4P2R2",
        "B4N1K8"
    )

    def __init__(self, client : commands.Bot):
        self.client = client

    def is_explode(self, force : bool = False) -> Union[ExplosionReason, False]:

        # Simple way to add code for a forced explosion
        explosion_reason = False if not force else ExplosionReason.GENERIC_EXPLOSION

        # If we didn't force an explosion
        if not explosion_reason:

        
    @app_commands.command(
        name = "feed",
        description = "Feed Bert some cheese!"
    )
    async def cheese_feed(self, interaction : discord.Interaction):

        if interaction.user == self.last_fed_by:
            return await interaction.response.send_message("<:humberto:1043390721023021106> Bert desires someone else's Cheese.")

        self.cheese_fed += 1
        self.last_fed_by = interaction.user

        if self.is_explode():

            self.last_explosion = datetime.now()
            self.last_explosion_high_score = self.cheese_fed

            if self.last_explosion_high_score > self.high_score or self.high_score == 0:
                self.high_score = self.last_explosion_high_score
                self.high_score_on = self.last_explosion

            self.cheese_fed = 0
            self.last_fed_by = None

            return await interaction.response.send_message(
                f"<a:GarfBop:1043390081924333608> Bert exploded.\nThe score was `{self.last_explosion_high_score:,}`.\nThe high score is `{self.high_score}` achieved <t:{int(self.high_score_on.timestamp())}:R>"
            )


        return await interaction.response.send_message(
            f"<a:ratboingboing:1045359237234176010> You have fed Bert.\nBert has been fed `{self.cheese_fed:,}` times this session."
        )

async def setup(client : commands.Bot):
    await client.add_cog(
        CheeseCog(client)
    )