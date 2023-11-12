from nextcord import Interaction, Member, User, ui

__all__: tuple[str, ...] = ("BaseView",)


class BaseView(ui.View):
    def __init__(self, user: User | Member, **kwargs) -> None:
        super().__init__(**kwargs)
        self.user = user

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.user.id:
            await interaction.send(
                "The button can only be accessed by the person issuing the command!", ephemeral=True, delete_after=5
            )
            return False
        return True
