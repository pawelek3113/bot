import typing as t
from datetime import datetime
from .views.ServerInfoView import ServerInfoView
from .views.UserInfoView import UserInfoView
from nextcord import Embed, Interaction, Member, slash_command
from nextcord.ext import application_checks
from nextcord.utils import format_dt

from . import BaseCog

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class Info(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)

    @slash_command(name="user", description="Check someone's info")
    @application_checks.guild_only()
    async def user_info(self, interaction: Interaction, member: Member):
        roles: list[str] = [role.mention for role in member.roles[1:]]
        role_count = len(roles)

        if role_count == 0:
            roles.append("```No roles```")

        roles.reverse()

        if len(roles) > 15:
            roles = roles[:15]

        embed = (
            Embed(color=member.color, title="User info", timestamp=datetime.utcnow())
            .add_field(name="Username", value=f"```{member.name}```")
            .add_field(name="User ID", value=f"```{member.id}```", inline=True)
            .add_field(name=f"Roles (15 max)", value=f"{' '.join(roles)}", inline=False)
            .add_field(
                name="Display name",
                value=f"```{member.display_name}```",
                inline=True,
            )
            .add_field(name="Is a bot?", value=f"```{'Yes' if member.bot else 'No'}```", inline=True)
            .add_field(
                name="Joined on: ",
                value=f"{format_dt(member.joined_at)} ({format_dt(member.joined_at, 'R')})",
                inline=False,
            )
            .add_field(
                name="Account created on: ",
                value=f"{format_dt(member.created_at)} ({format_dt(member.created_at, 'R')})",
                inline=False,
            )
        ).set_thumbnail(member.display_avatar)

        await interaction.send(embed=embed, view=UserInfoView(member=member))

    @slash_command(name="server", description="Check server's info")
    @application_checks.guild_only()
    async def server_info(self, interaction: Interaction):
        server = interaction.guild

        roles: list[str] = [role.mention for role in server.roles[1:]]
        role_count = len(roles)
        roles.reverse()

        if role_count > 10:
            roles = roles[:10]

        ban_count = len([ban async for ban in server.bans()])

        categories = [category for category in server.categories]
        channels = [channel.mention for channel in server.channels if channel not in categories]

        channel_count = len(channels)

        if channel_count > 10:
            channels = channels[:10]

        embed = (
            Embed(color=0x3461BB, title="Server info", timestamp=datetime.utcnow())
            .add_field(name="Name", value=f"```{server.name}```")
            .add_field(name="Server ID", value=f"```{server.id}```", inline=True)
            .add_field(name="Roles (max 10)", value=f"{' '.join(roles)}", inline=False)
            .add_field(name="Role count", value=f"```{role_count}```", inline=True)
            .add_field(name="Member count", value=f"```{server.member_count}```", inline=True)
            .add_field(name="Bot count", value=f"```{len(server.bots)}```", inline=True)
            .add_field(name="Owner", value=f"```{server.owner.name}```", inline=False)
            .add_field(name="Ban count", value=f"```{ban_count}```", inline=True)
            .add_field(name="Server language", value=f"```{server.preferred_locale}```", inline=True)
            .add_field(name="Channels (max 10)", value=f"{' '.join(channels)}", inline=False)
            .add_field(name="Tier", value=f"```{server.premium_tier}```", inline=True)
            .add_field(name="Nitro boosts", value=f"```{server.premium_subscription_count}```", inline=True)
            .add_field(
                name="Server created on: ",
                value=f"{format_dt(server.created_at)} ({format_dt(server.created_at, 'R')})",
                inline=False,
            )
        ).set_thumbnail(server.icon)

        await interaction.send(embed=embed, view=ServerInfoView())

    @slash_command(description="Check channel's info")
    @application_checks.guild_only()
    async def channel_info(self, interaction: Interaction):
        ...
