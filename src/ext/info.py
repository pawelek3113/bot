import typing as t
from datetime import datetime

from nextcord import (
    Embed, ForumChannel, Interaction, Member, StageChannel, TextChannel, Thread, VoiceChannel, slash_command,
)
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
            .add_field(name="ID", value=f"```{member.id}```", inline=True)
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
            .add_field(name="ID", value=f"```{server.id}```", inline=False)
            .add_field(name="Member count", value=f"```{server.member_count}```", inline=True)
            .add_field(name="Bot count", value=f"```{len(server.bots)}```", inline=True)
            .add_field(name="Owner", value=f"```{server.owner.name}```", inline=False)
            .add_field(name="Role count", value=f"```{role_count}```", inline=True)
            .add_field(name="Ban count", value=f"```{ban_count}```", inline=True)
            .add_field(name="Server language", value=f"```{server.preferred_locale}```", inline=True)
            .add_field(name="Nitro tier", value=f"```{server.premium_tier}```", inline=True)
            .add_field(name="Nitro boosts", value=f"```{server.premium_subscription_count}```", inline=True)
            .add_field(
                name="Server created on: ",
                value=f"{format_dt(server.created_at)} ({format_dt(server.created_at, 'R')})",
                inline=False,
            )
        ).set_thumbnail(server.icon)

        await interaction.send(embed=embed, view=ServerInfoView(user=interaction.user))

    @slash_command(name="channel", description="Check channel's info")
    @application_checks.guild_only()
    async def channel_info(
        self,
        interaction: Interaction,
        channel: TextChannel | VoiceChannel | StageChannel | ForumChannel | None,
    ):
        if not channel:
            channel = interaction.channel

        embed = (
            Embed(color=0x3461BB, title="Channel info", timestamp=datetime.utcnow())
            .add_field(name="Name", value=f"```{channel.name}```")
            .add_field(name="ID", value=f"```{channel.id}```", inline=False)
            .add_field(name="Type", value=f"```{channel.type}```", inline=True)
            .add_field(name="NSFW", value=f"```{'Yes' if channel.is_nsfw() else 'No'}```", inline=True)
        )

        if not isinstance(channel, (VoiceChannel, ForumChannel, Thread)):
            if channel.topic is not None:
                embed.add_field(
                    name="Topic",
                    value=f"```{channel.topic if len(channel.topic) < 200 else f'{channel.topic[:200]}...'}```",
                    inline=False,
                )

        if channel.category is not None:
            embed.add_field(name="Category", value=f"```{channel.category}```", inline=False)

        embed.add_field(name="Jump URL", value=f"{channel.jump_url}", inline=False)

        if not isinstance(channel, (VoiceChannel, StageChannel)):
            embed.add_field(name="Slowmode delay", value=f"```{channel.slowmode_delay}```", inline=True)
        else:
            embed.add_field(name="Bitrate", value=f"```{channel.bitrate}kbps```", inline=False)
            embed.add_field(
                name="User limit",
                value=f"```{channel.user_limit if channel.user_limit != 0 else 'No limit'}```",
                inline=False,
            )
            embed.add_field(
                name="Region",
                value=f"```{str(channel.rtc_region).capitalize() if channel.rtc_region else 'Automatic'}```",
                inline=False,
            )

        embed.add_field(
            name="Channel created on: ",
            value=f"{format_dt(channel.created_at)} ({format_dt(channel.created_at, 'R')})",
            inline=False,
        )

        await interaction.send(embed=embed)
