from discord import ui
from discord import TextStyle, Interaction
from objects.achievements.AchievementManager import AchievementManager

class AchievementCreator(ui.Modal, title="Achievement Creator"):

    achieveman : AchievementManager

    def __init__(self, achieveman : AchievementManager) -> None:
        self.achieveman = achieveman

        super().__init__()

    name = ui.TextInput(
        label = "Achievement Name",
        placeholder = "Mediocre Fisher",
        required = True
    )

    taskline = ui.TextInput(
        label = "Taskline",
        placeholder = "Catch %(req) Salmon!",
        style = TextStyle.paragraph,
        required = True
    )

    requirement = ui.TextInput(
        label = "Requirement (integer)",
        placeholder = "25",
        required = True,
    )

    custom_asset = ui.TextInput(
        label = "Custom Asset ID",
        placeholder = "FISH_SALMON"
    )

    async def on_submit(self, interaction: Interaction, /) -> None:

        return await interaction.response.send_message("Bing Bong!")