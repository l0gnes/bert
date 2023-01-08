from discord.ext import commands
from discord import app_commands
from discord import Interaction, Embed
from random import randint

class NumberGuesser(commands.Cog):

    number_to_guess : int

    def __init__(self, client : commands.Bot) -> None:
        self.client = client

        self.range = (0, 50)
        self.number_to_guess = randint(*self.range)


    @app_commands.command(
        name = "guess",
        description = "Number guesser"
    )
    @app_commands.describe(
        number = "The number you want to guess"
    )
    async def numberguesser_guess(self, interaction : Interaction, number : int) -> None:
        
        # The number is too big
        if number > self.number_to_guess:
            return await interaction.response.send_message(
                embed = Embed(
                    description="<a:catno:1052727494899412993> Too big",
                    colour = 0xFF0000
                ),
                ephemeral=True
            )

        elif number < self.number_to_guess:
            return await interaction.response.send_message(
                embed = Embed(
                    description = "<a:catno:1052727494899412993> Too small",
                    colour = 0xFF0000
                ),
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                content = f"{interaction.user.mention} **Guessed the number!**",
                embed = Embed(
                    description=f"<a:catyes:1052727468001349712> Just right, the number was `{self.number_to_guess}`",
                    colour=0x00FF00
                ).set_footer(
                    text = "A new number has been assigned (%d - %d)" % self.range
                )
            )

            self.number_to_guess = randint(*self.range)

            return

async def setup(client : commands.Bot):
    await client.add_cog(NumberGuesser(client))