import typing as t
from datetime import datetime

from nextcord import Embed, Interaction, Member, slash_command
from nextcord.ext import application_checks
from nextcord.utils import format_dt

from ..views.ServerInfoView import ServerInfoView
from ..views.UserInfoView import UserInfoView
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

        if not roles:
            roles = [
                "```No roles```",
            ]

        roles.reverse()
        roles = roles[:15]

        embed = (
            Embed(color=member.color, title="User info", timestamp=datetime.utcnow())
            .add_field(name="Username", value=f"```{member.name}```")
            .add_field(name="User ID", value=f"```{member.id}```", inline=True)
            .add_field(name="Roles (15 max)", value=f"{' '.join(roles)}", inline=False)
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

        await interaction.send(embed=embed, view=UserInfoView(user=interaction.user, member=member))

    @slash_command(name="server", description="Check server's info")
    @application_checks.guild_only()
    async def server_info(self, interaction: Interaction):
        server = interaction.guild

        role_count = len(server.roles[1:])

        ban_count = len([ban async for ban in server.bans()])

        embed = (
            Embed(color=0x3461BB, title="Server info", timestamp=datetime.utcnow())
            .add_field(name="Name", value=f"```{server.name}```")
            .add_field(name="Server ID", value=f"```{server.id}```", inline=False)
            .add_field(name="Member count", value=f"```{server.member_count}```", inline=True)
            .add_field(name="Bot count", value=f"```{len(server.bots)}```", inline=True)
            .add_field(name="Owner", value=f"```{server.owner.name}```", inline=False)
            .add_field(name="Role count", value=f"```{role_count}```", inline=True)
            .add_field(name="Ban count", value=f"```{ban_count}```", inline=True)
            .add_field(name="Server language", value=f"```{server.preferred_locale}```", inline=True)
            .add_field(name="Nitro  Tier", value=f"```{server.premium_tier}```", inline=True)
            .add_field(name="Nitro boosts", value=f"```{server.premium_subscription_count}```", inline=True)
            .add_field(
                name="Server created on: ",
                value=f"{format_dt(server.created_at)} ({format_dt(server.created_at, 'R')})",
                inline=False,
            )
        ).set_thumbnail(server.icon)

        await interaction.send(embed=embed, view=ServerInfoView(user=interaction.user))

    @slash_command(description="Check channel's info")
    @application_checks.guild_only()
    async def channel_info(self, interaction: Interaction):
        ...
