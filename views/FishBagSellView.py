from discord import ui
from discord import User, Interaction, ButtonStyle, Embed
from objects.fishing.FishingManager import FishingManager
from objects import EconomyManager
from typing import List, Tuple, Union
from objects.fishing.Fish import Fish
from objects.fishing.Junk import Junk

class FishbagSellView(ui.View):

    user : User
    fishman : FishingManager
    ecoman : EconomyManager
    worth : int
    bag : List[Tuple[Union[Fish, Junk], int]]

    def __init__(
        self,
        fishman : FishingManager,
        bag : List[Tuple[Union[Fish, Junk], int]],
        user : User
    ) -> None:
        self.fishman = fishman
        self.bag = bag
        self.user = user

        self.ecoman = fishman.ecoman

        self.worth = self.fishman.fishlog.calculate_bag_value(self.bag)
        self.is_bag_empty = len(self.bag) < 1

        super().__init__()

        if not self.is_bag_empty:
            
            temp = ui.Button(
                style = ButtonStyle.green,
                emoji = self.fishman.client.emoji_map.fetch_first("DABLOONS"),
                label = f"Sell Fish for {self.worth:,} dabloons"
            )
            temp.callback = self.sell_callback

            self.add_item(temp)

    async def sell_callback(self, interaction : Interaction) -> None:

        if interaction.user != self.user:
            return await interaction.response.send_message(
                "Open your own fishbag and use the sell button!",
                ephemeral = True
            )
            
        await self.fishman.empty_user_fish_bag(self.user)
        await self.ecoman.add_balance(self.user, self.worth)

        await interaction.response.send_message(
            embed = Embed(
                description = f"{self.fishman.client.emoji_map.fetch_first('DABLOONS')} Sold fish for {self.worth} dabloons",
                colour=0xFFFF00
            ),
            ephemeral = True
        )

        self.stop()