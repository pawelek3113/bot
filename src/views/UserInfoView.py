from nextcord import Interaction, Member, ui

from . import BaseView


class UserRolesBtn(ui.Button["UserInfoView"]):
    def __init__(self, member: Member) -> None:
        super().__init__(emoji="🎭")
        self.member = member

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        roles: list[str] = [role.mention for role in self.member.roles[1:]]
        roles.reverse()
        if roles:
            msg = f"```{self.member.name} roles ({len(roles)}): ```\n" + ", ".join(roles)
        else:
            msg = f"{self.member.name} has no roles in {interaction.guild.name}."
        await interaction.send(msg, ephemeral=True)


class UserBanBtn(ui.Button["UserInfoView"]):
    def __init__(self, member: Member, **kwargs) -> None:
        super().__init__(emoji="🚫", **kwargs)
        self.member = member

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()

        if self.member is None:
            await interaction.send("Something went wrong.", ephemeral=True)
            return
        if interaction.user == self.member:
            await interaction.send(f"{self.member.mention}, you can't ban yourself!", ephemeral=True)
            return

        await self.member.ban(reason="No reason given", delete_message_seconds=0)
        await interaction.send(f"{interaction.user.mention} banned {self.member.display_name}!")


class UserInfoView(BaseView):
    def __init__(self, user: Member, member: Member, **kwargs) -> None:
        super().__init__(user=user, **kwargs)
        self.user = user
        self.member = member

        if self.user.guild_permissions.administrator is not True:
            self.add_item(UserRolesBtn(member=member))
            self.add_item(UserBanBtn(member=member, disabled=True))
        else:
            self.add_item(UserRolesBtn(member=member))

            if self.user != member:
                self.add_item(UserBanBtn(member=member))
            else:
                self.add_item(UserBanBtn(member=member, disabled=True))
