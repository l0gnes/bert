
import discord
from discord.ext import commands
from discord import app_commands

from bert import BertBot
from objects.fishing.FishingManager import FishingManager
from objects.fishing.FishLogicHandler import FishLogicHandler
from objects.ASCIIProgressBar import ASCIIProgressBar
from objects.fishing.exceptions import FishingBagIsFull 
from objects.fishing.SpecialFishEvent import SpecialFishEvent
import math
import random
from typing import Optional
from views.FishBagSellView import FishbagSellView

class FishingCog(commands.Cog):

    client : "BertBot"

    fishing_command_group = app_commands.Group(name="fishing", description="balls")

    def __init__(self, client : "BertBot") -> None:
        self.client = client

        self.fishlogic = FishLogicHandler()
        self.fishman = FishingManager(self.client, fish_logic = self.fishlogic)

    @fishing_command_group.command(
        name = "profile",
        description="View fishing profiles"
    )
    @app_commands.describe(
        user = "The user you wish to view the profile of, You don't need to specify this when looking at yourself."
    )
    async def fishing_fishing(self, interaction : discord.Interaction, *, user : Optional[discord.User] = None) -> None:

        user_to_check = user if user is not None else interaction.user

        fishingAccount = await self.fishman.fetch_partial_fishing_account(user_to_check)

        fishing_rod_emoji = self.client.emoji_map.fetch_first(
            fishingAccount.fishing_rod.asset
        )

        fish_box_emoji = self.client.emoji_map.fetch_first("FISH_BOX")
        treasure_emoji = self.client.emoji_map.fetch_first("GOLD_GOBLET")
        star_emoji = self.client.emoji_map.fetch_first("STAR")
        bag_emoji = self.client.emoji_map.fetch_first("BACKPACK")

        strings = [
            f"{fishing_rod_emoji} Current Rod: **{fishingAccount.fishing_rod.name}**",
            f"{fish_box_emoji} Fish Caught: **{fishingAccount.fish_caught:,}**",
            f"{bag_emoji} Fishing Bag Size: **{fishingAccount.bag_size:,} slots**",
            #f"{treasure_emoji} Treasure Fished: **{fishingAccount.treasure_fished:,}**"
        ]

        exp_offset = fishingAccount.experience_for_level(fishingAccount.level - 1)
        bar = ASCIIProgressBar.bar((fishingAccount.experience - exp_offset) / (fishingAccount.experience_to_next_level - exp_offset))

        return await interaction.response.send_message(
            embed = discord.Embed(
                colour=0xFFFF00,
                description="\n".join(strings)
            ).set_author(
                name = f"{user_to_check.display_name}'s Fishing Profile",
                icon_url = user_to_check.display_avatar
            ).add_field(
                name = f"{star_emoji} Current Level: {fishingAccount.level}",
                value = f"Progress: {math.floor(fishingAccount.experience - exp_offset):,}xp / {math.ceil(fishingAccount.experience_to_next_level - exp_offset):,}xp\n`{bar}`"
            )
        )

    @app_commands.command(
        name = "catch",
        description = "Catch a fish"
    )
    @app_commands.checks.cooldown(3, 30, key=lambda i: (i.guild_id, i.user.id))
    async def fishing_catch(self, interaction : discord.Interaction) -> None:
        fishingAccount = await self.fishman.fetch_partial_fishing_account(interaction.user)

        special_event = self.fishlogic.special_events_hook()

        additional_dabloons = 0
        fish_mult = 1
        if special_event == SpecialFishEvent.CRITICAL_HOOK:
            fish_mult = 5
        elif special_event == SpecialFishEvent.DABLOON_DIVE:
            additional_dabloons = random.randint(30, 80)
            await self.client.ecoman.add_balance(interaction.user, additional_dabloons)

        amount, fish = self.fishlogic.catch_fish(
            fishingAccount,
            force_catch = None if special_event != SpecialFishEvent.CRITICAL_HOOK else "FISH"
        )

        amount *= fish_mult

        free_space = await self.fishman.bag_count_free_space(interaction.user)

        if free_space == 0:
            raise FishingBagIsFull

        elif amount > free_space:
            amount = free_space # Fills bag instead of overflows bag

        await self.fishman.add_fish_to_bag(
            user = interaction.user,
            amount = amount,
            fish = fish,
            bypass_ensure = True
        )

        await self.fishman.increment_fish_caught_statistic(interaction.user, amount, bypass_ensure=True)

        experience_earned = self.fishlogic.calculate_experience_earned(
            fishingAccount,
            fish, amount
        )

        # Check for level up
        levelled_up = fishingAccount.will_level_up_check(experience_earned)

        await self.fishman.increment_fishing_experience(interaction.user, experience_earned, bypass_ensure = True)

        e = discord.Embed(
            colour = 0xFFFF00,
            description = f"{interaction.user.display_name} caught **{amount}x {self.client.emoji_map.fetch_first(fish.asset)} {fish.name}**!"
        )

        if special_event == SpecialFishEvent.CRITICAL_HOOK:
            e.description += f"\n{self.client.emoji_map.fetch_first('CRIT_HOOK')} **Critical Hook!** You caught a lot of fish!"
        
        elif special_event == SpecialFishEvent.DABLOON_DIVE:
            e.description += f"\n{self.client.emoji_map.fetch_first('DABLOONS')} **Dabloon Dive!** You fished up {additional_dabloons:,} dabloons!"

        if levelled_up:
            e.set_footer(
                text = f"You levelled up! You're now level {fishingAccount.level + 1}!",
                icon_url = interaction.user.display_avatar
            )

        return await interaction.response.send_message(
            embed = e
        )


    @fishing_catch.error
    async def fishing_catch_error_handler(
        self,
        interaction : discord.Interaction,
        error : Exception
    ) -> None:

        if isinstance(error, FishingBagIsFull):

            bag_emoji = self.client.emoji_map.fetch_first("BACKPACK")

            return await interaction.response.send_message(
                embed = discord.Embed(
                    description = f"{bag_emoji} You can't catch anymore fish! Your fishing bag is full!",
                    color = 0xFF0000
                ).set_footer(
                    icon_url = interaction.user.avatar,
                    text = "You can view your bag with: /fishing bag"
                ),
                ephemeral = True
            )

        elif isinstance(error, app_commands.CommandOnCooldown):

            cooldown_emoji = self.client.emoji_map.fetch_first("HOURGLASS")

            return await interaction.response.send_message(
                embed = discord.Embed(
                    colour = 0xFF0000,
                    description = f"{cooldown_emoji} Seems like no fish are biting for you right now, try again in a few seconds."
                ),
                ephemeral = True
            )

        raise error # Raises error anyways if no handler exists

    @fishing_command_group.command(
        name = "bag",
        description = "View your fishing bag"
    )
    async def fishing_fishing_bag(
        self, interaction : discord.Interaction
    ) -> None:
        
        fish_bag = await self.fishman.fetch_user_fish_bag(interaction.user)
        fishing_user = await self.fishman.fetch_partial_fishing_account(interaction.user, bypass_ensure=True)

        used_bag_space = sum([
            f[1] for f in fish_bag
        ])
        bag_emoji = self.client.emoji_map.fetch_first("BACKPACK")

        string_builder = [
            f"**{amount:,}x** {self.client.emoji_map.fetch_first(fishable.asset)} {fishable.name}" for fishable, amount in fish_bag
        ]

        fishbagView = FishbagSellView(
            self.fishman, fish_bag, interaction.user
        )

        fishbagView.message = await interaction.response.send_message(
            embed = discord.Embed(
                colour = 0xFFFF00,
                description= "\n".join(string_builder) if len(string_builder) else "You have no fish!",
            ).set_author(
                name = f"{interaction.user.display_name}'s Fishing Bag",
                icon_url = interaction.user.display_avatar
            ).add_field(
                name = f"{bag_emoji} Bag Capacity: ({used_bag_space}/{fishing_user.bag_size})",
                value = "`" + ASCIIProgressBar.bar(used_bag_space / fishing_user.bag_size) + "`"
            ),
            view = fishbagView,
            ephemeral = True
        )

async def setup(client):
    await client.add_cog(
        FishingCog(client)
    )