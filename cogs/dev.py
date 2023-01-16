import discord
from discord.ext import commands
from discord import app_commands

from bert import BertBot
from objects.EconomyManager import EconomyManager
from objects.fishing.FishingManager import FishingManager
from objects.tags.TagManager import TagManager
from objects.CommandTreeCacher import CommandTreeCacher
from modals.TagCreation import TagCreationModal

from modals.AchievementCreator import AchievementCreator

from json import dumps, loads

class DeveloperCog(commands.GroupCog, name="dev"):

    def __init__(self, client : "BertBot"):
        self.client = client
        super().__init__()

        self.app_command.interaction_check = self.interaction_check

        self.ecoman = EconomyManager(self.client)
        self.fishman = FishingManager(self.client)
        self.tagman = TagManager(self.client)

    async def interaction_check(self, interaction : discord.Interaction) -> bool:
        return interaction.user.id in self.client.developer_ids

    async def cog_app_command_error(
        self, 
        interaction: discord.Interaction, 
        error: app_commands.AppCommandError
    ) -> None:

        if isinstance(error, app_commands.errors.CheckFailure):

            return await interaction.response.send_message(
                "You cannot run this command.",
                ephemeral=True
            )

        raise error
        return await super().cog_app_command_error(interaction, error)

    @app_commands.command(
        name = "test",
        description = "Test Command"
    )
    async def dev_test(self, interaction : discord.Interaction, title : str) -> None:
        await interaction.response.send_modal(
            TagCreationModal(self.tagman, title)
        )

    @app_commands.command(
        name="tagtest",
        description="Try to fetch the test tag. Make sure it exists!"
    )
    async def dev_tagtest(self, interaction : discord.Interaction) -> None:
        t = await self.tagman.fetch_tag_by_title(interaction.guild, "cum")
        em = await t.create_embed()
        return await interaction.response.send_message(
            embed = em,
            ephemeral = True
        )

    @app_commands.command(
        name = "ecogive",
        description = "Give a user a certain amount of money"
    )
    async def dev_ecogive(self, interaction : discord.Interaction, user : discord.User, amount : int) -> None:
        new_bal = await self.ecoman.add_balance(user, amount)
        return await interaction.response.send_message(
            f"{user.mention}'s balance has been updated.\n**They now have {new_bal:,} dabloons.**"
        )

    @app_commands.command(
        name = "setfishingrod",
        description = "Sets the fishing rod for a user"
    )
    async def dev_setfishingrod(
        self, 
        interaction : discord.Interaction, 
        user : discord.User, 
        rod : int
    ) -> None:

        parsed_rod = self.fishman.fishing_rods.get(rod, None)

        if parsed_rod is None:
            return await interaction.response.send_message(
                "That fishing rod id does not exist", ephemeral=True
            )

        await self.fishman.set_fishing_rod(user, rod)

        return await interaction.response.send_message(
            f"{user.mention}'s fishing rod has been set to: {self.client.emoji_map.fetch_first(parsed_rod.asset)} **{parsed_rod.name}**",
            ephemeral = True
        )

    @app_commands.command(
        name = "fishingpower",
        description = "Fetches the calculated fishing power for a user"
    )
    async def dev_fishingpower(
        self,
        interaction : discord.Interaction,
        user : discord.User
    ) -> None:
        fa = await self.fishman.fetch_partial_fishing_account(user)

        return await interaction.response.send_message(
            f"{user.display_name} has a calculated fishing power of: {fa.calculated_fishing_power}"
        )

    @app_commands.command(
        name = "guilds",
        description = "Views the guilds that this bot is in"
    )
    async def dev_guilds(
        self,
        interaction : discord.Interaction
    ) -> None:
        guild_list = []

        async for guild in self.client.fetch_guilds():
            guild_list.append(
                (guild.name, guild.id)
            )

        joined_list = "\n".join(
            [
                "**{0}** | `{1}`".format(*g) for g in guild_list
            ]
        )

        return await interaction.response.send_message(
            joined_list,
            ephemeral = True
        )

    @app_commands.command(
        name = "jsontree",
        description = "Generates a json format of the command tree"
    )
    async def dev_jsontree(
        self, interaction : discord.Interaction
    ) -> None:
        ctc = CommandTreeCacher(self.client.tree)

        generated_tree = ctc.generate_json_tree()

        tree_to_string = dumps(generated_tree, ensure_ascii=True, indent=4)

        return await interaction.response.send_message(
            "```json\n%s```" % (tree_to_string)
        )

    @app_commands.command(
        name = "sqlexec",
        description = "Executes a raw SQL query"
    )
    async def dev_sqlexec(
        self,
        interaction : discord.Interaction,
        query : str
    ) -> None:
        
        use_fetch = (True if any(
            map(
                lambda n: n in query.upper(),
                [
                    "SELECT", "RETURNING"
                ]
            )
        ) else False)

        if use_fetch:
            resp = await self.client.pool.fetch(
                query
            )

            return await interaction.response.send_message(
                embed = discord.Embed(
                    description=f"`{query}`\n```json\n{dumps(list(map(dict, resp)), indent=4)}```"
                ).set_footer(
                    text = "Query returned results",
                    icon_url = interaction.user.display_avatar
                )
            )

        else:
            await self.client.pool.execute(query)

            return await interaction.response.send_message(
                "SQL Executed.", ephemeral = True
            )

    @app_commands.command(
        name = "achvcreate",
        description = "Create a new achievement."
    )
    async def dev_achvcreate(self, interaction : discord.Interaction) -> None:

        return await interaction.response.send_modal(
            AchievementCreator(self.client.achieveman)
        )


async def setup(client):
    await client.add_cog(
        DeveloperCog(
            client = client
        )
    )