import typing as t
from datetime import datetime

from nextcord import Embed, Interaction, Member, Permissions, SlashOption, slash_command
from nextcord.ext import application_checks
from nextcord.utils import format_dt

from . import BaseCog

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class Info(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)

    @slash_command(description="Check someone's info")
    @application_checks.guild_only()
    async def user_info(self, interaction: Interaction, member: Member):
        embed = (
            Embed(color=member.color, title="User info", timestamp=datetime.utcnow())
            .add_field(name="Username", value=f"```{member.name}```")
            .add_field(name="User ID", value=f"```{member.id}```", inline=True)
            .add_field(name="Roles", value=f"{' '.join([role.mention for role in member.roles])}", inline=False)
            .add_field(
                name="Display name",
                value=f"```{member.display_name if member.display_name is not member.name else 'No display name'}```",
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

        await interaction.send(embed=embed)

    @slash_command(description="Check server's info")
    @application_checks.guild_only()
    async def server_info(self, interaction: Interaction):
        ...

    @slash_command(description="Check channel's info")
    @application_checks.guild_only()
    async def channel_info(self, interaction: Interaction):
        ...
