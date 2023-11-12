from nextcord import Interaction, Member, ui

from . import BaseView


class ServerRolesBtn(ui.Button["ServerInfoView"]):
    def __init__(self, **kwargs) -> None:
        super().__init__(emoji="🎭", **kwargs)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        roles: list[str] = [role.mention for role in interaction.guild.roles[1:]]
        roles.reverse()

        if roles:
            msg = f"```{interaction.guild.name} roles ({len(roles)}): ```\n" + ", ".join(roles)
        else:
            msg = f"There aren't any roles in {interaction.guild.name}."
        await interaction.send(msg, ephemeral=True)


class ServerChannelsBtn(ui.Button["ServerInfoView"]):
    def __init__(self, **kwargs) -> None:
        super().__init__(emoji="🗂", **kwargs)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        categories = [category for category in interaction.guild.categories]
        channels = [channel.mention for channel in interaction.guild.channels if channel not in categories]

        if channels:
            msg = f"```{interaction.guild.name} channels ({len(channels)}): ```\n" + ", ".join(channels)
        else:
            msg = f"There aren't any channels in {interaction.guild.name}."
        await interaction.send(msg, ephemeral=True)


class ServerMembersBtn(ui.Button["ServerInfoView"]):
    def __init__(self, **kwargs) -> None:
        super().__init__(emoji="👤", **kwargs)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        members: list[str] = [member.mention for member in interaction.guild.members]
        members.sort()

        msg = f"```{interaction.guild.name} members ({len(members)}): ```\n" + ", ".join(members)
        await interaction.send(msg, ephemeral=True)


class ServerFeaturesBtn(ui.Button["ServerInfoView"]):
    def __init__(self, **kwargs) -> None:
        super().__init__(emoji="📎", **kwargs)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        features = [f'- {feature.replace("_", " ").capitalize()}' for feature in interaction.guild.features]

        if features:
            msg = f"```{interaction.guild.name} features ({len(features)}): ```\n" + "\n".join(features)
        else:
            msg = f"There are no features in {interaction.guild.name}."
        await interaction.send(msg, ephemeral=True)


class ServerInfoView(BaseView):
    def __init__(self, user: Member, **kwargs) -> None:
        super().__init__(user=user, **kwargs)

        self.add_item(ServerRolesBtn())
        self.add_item(ServerChannelsBtn())
        self.add_item(ServerMembersBtn())
        self.add_item(ServerFeaturesBtn())
