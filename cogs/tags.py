import discord
from discord.ext import commands
from discord import app_commands

from bert import BertBot
from objects.tags.TagManager import TagManager
from modals.TagCreation import TagCreationModal

class TagCog(commands.Cog):

    client : BertBot
    tagman : TagManager

    def __init__(self, client : "BertBot") -> None:
        self.client = client
        self.tagman = TagManager(self.client)

        super().__init__()

    @app_commands.command(
        name = "tag",
        description = "View a tag"
    )
    async def tags_tag(
        self, 
        interaction : discord.Interaction,
        title : str
    ) -> None:

        tag = await self.tagman.fetch_tag_by_title(interaction.guild, title)

        if tag is None:
            return await interaction.response.send_message(
                "⚠️ That tag does not exist in this guild!",
                ephemeral = True
            )
        
        tag_embed = await tag.create_embed()

        return await interaction.response.send_message(
            embed = tag_embed
        )

    @app_commands.command(
        name = "createtag",
        description = "Create a new tag"
    )
    async def tags_createtag(self, interaction : discord.Interaction, title : str) -> None:

        check = await self.tagman.ensure_tag_exists(
            interaction.guild, title
        )

        if check:
            return await interaction.response.send_message(
                "⚠️ That tag title is already in use. Please try another one!",
                ephemeral = True
            )

        return await interaction.response.send_modal(
            TagCreationModal(self.tagman, title)
        )

    @app_commands.command(
        name = "edittag",
        description = "Edits a tag if you own it"
    )
    async def tags_edittag(self, interaction : discord.Interaction, title : str) -> None:
        
        ownership_check = await self.tagman.ensure_user_owns_tag(
            interaction.user, title, guild = interaction.guild
        )

        if not ownership_check:
            return await interaction.response.send_message(
                "⚠️ You either do not own this tag, or it doesn't exist!",
                ephemeral = True
            )

        tag = await self.tagman.fetch_tag_by_title(interaction.guild, title)

        return await interaction.response.send_modal(
            TagCreationModal.create_from_tag_object(tag)
        )

    @app_commands.command(
        name = "deletetag",
        description = "Deletes a tag if you own it."
    )
    async def tags_deletetag(
        self,
        interaction : discord.Interaction,
        title : str
    ) -> None:

        ownership_check = await self.tagman.ensure_user_owns_tag(
            interaction.user, title, guild = interaction.guild
        )

        if not ownership_check:
            return await interaction.response.send_message(
                "⚠️ You either do not own this tag, or it doesn't exist!",
                ephemeral = True
            )

        await self.tagman.delete_tag(
            interaction.user,
            title, 
            guild = interaction.guild
        )

        return await interaction.response.send_message(
            f'✅ The `"{title.lower()}"` tag has been deleted from this server!',
            ephemeral = True
        )
        

async def setup(client : BertBot):
    await client.add_cog(
        TagCog(client)
    )
        

