from discord import ui
from discord import TextStyle, Interaction
from objects.tags.TagManager import TagManager
from objects.tags.Tag import Tag

class TagCreationModal(ui.Modal):

    tagman : TagManager
    tagtitle : str

    update_mode : bool = False

    def __init__(
        self,
        tagman : TagManager,
        _title : str,
        *,
        update_mode : bool = False
    ) -> None:
        self.tagman = tagman
        self.tagtitle = _title.lower()
        self.update_mode = update_mode

        super().__init__(
            title = f"Creating Tag: '{self.tagtitle}'"
        )

    @classmethod
    def create_with_data(
        cls, 
        tagman : TagManager, 
        _title : str, 
        _content : str, 
        _image : str
    ) -> "TagCreationModal":
        
        new_obj = cls(tagman, _title, update_mode = True)

        new_obj.content._underlying.value = _content
        new_obj.image._underlying.value = _image

        return new_obj

    @classmethod
    def create_from_tag_object(
        cls,
        tag : "Tag"
    ) -> "TagCreationModal":

        return TagCreationModal.create_with_data(
            tag.tagman,
            tag.title,
            tag.content,
            tag.imageurl
        )

    content = ui.TextInput(
        label = "Tag Content",
        placeholder = "This is my really cool tag!",
        style = TextStyle.paragraph,
        required = True
    )

    image = ui.TextInput(
        label = "Image URL",
        style = TextStyle.short,
        placeholder="https://upload.wikimedia.org/wikipedia/commons/d/d3/Rattus_norvegicus_-_Brown_rat_02.jpg",
        required=False
    )

    async def on_submit(self, interaction: Interaction) -> None:

        if self.update_mode:

            print("aaaaaaaa")

            guild = interaction.guild

            await self.tagman.update_tag(
                guild,
                self.tagtitle,
                content = self.content.value,
                image_url = self.image.value
            )

            return await interaction.response.send_message(
                "Tag succesfully updated!", ephemeral = True
            )

        await self.tagman.create_new_tag(
            interaction.user,
            self.tagtitle,
            self.content.value,
            image_url = self.image.value,
            guild = interaction.user.guild
        )

        return await interaction.response.send_message(
            f"Your new tag has been created! Use `/tag {self.tagtitle}` to view it!",
            ephemeral = True
        )

    async def on_error(self, interaction: Interaction, error: Exception, /) -> None:
        await interaction.response.send_message(
            "Tag creation cancelled.", ephemeral=True
        )
        raise error