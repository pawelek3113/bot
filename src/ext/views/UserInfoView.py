from nextcord import Interaction, ui, Member


class UserInfoView(ui.View):
    def __init__(self, member: Member, **kwargs) -> None:
        super().__init__(**kwargs)
        self.member = member

    @ui.button(label="All roles")
    async def get_roles(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        roles: list[str] = [role.mention for role in self.member.roles[1:]]
        roles.reverse()
        if len(roles) != 0:
            msg = f"```{self.member.name} roles ({len(roles)}): ```\n" + ", ".join(roles)
        else:
            msg = f"{self.member.name} has no roles in {interaction.guild.name}."
        await interaction.send(msg, ephemeral=True)
