import discord
from discord.ext import commands
from discord import app_commands

from bert import BertBot

class EconomyCog(commands.Cog):

    client : "BertBot"

    def __init__(self, client : "BertBot") -> None:
        self.client = client

    @app_commands.command(
        name = "balance",
        description = "Check your balance"
    )
    async def eco_balance(self, interaction : discord.Interaction):

        balance = await self.client.ecoman.get_balance(interaction.user)
        dabloons_emoji = self.client.emoji_map.fetch_first("DABLOONS")

        return await interaction.response.send_message(
            embed = discord.Embed(
                colour = 0xFFFF00,
                description = f"{dabloons_emoji} You have {balance:,} dabloons"
            )
        )

    @app_commands.command(
        name = "pay",
        description = "Pay somebody some dabloons!"
    )
    @app_commands.describe(
        user = "The payee",
        amount = "The amount you want to pay"
    )
    async def eco_pay(self, interaction : discord.Interaction, user : discord.User, amount : int) -> None:
        
        sufficient_funds_check = await self.client.ecoman.has_balance(interaction.user, amount)

        if not sufficient_funds_check:
            return await interaction.response.send_message(
                "You don't have enough funds to do that.", ephemeral=True
            )

        new_payer_balance = await self.client.ecoman.deduct_balance(interaction.user, amount, bypass_ensure=True)
        await self.client.ecoman.add_balance(user, amount)

        dabloons_emoji = self.client.emoji_map.fetch_first("DABLOONS")
        return await interaction.response.send_message(
            embed = discord.Embed(
                colour = 0x00FF00,
                description = f"{dabloons_emoji} You paid {user.display_name} {amount:,} dabloons!"
            ).set_footer(
                text = f"You now have {new_payer_balance:,} dabloons.",
                icon_url = interaction.user.display_avatar
            )
        )

async def setup(client : BertBot):
    await client.add_cog(
        EconomyCog(client)
    )