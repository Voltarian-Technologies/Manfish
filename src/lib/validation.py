"""
Permission and input validation utilities
"""

import discord
from typing import Optional

def has_admin_permissions(interaction: discord.Interaction) -> bool:
    """Check if user has admin permissions"""
    if not interaction.guild:
        return False
    
    member = interaction.guild.get_member(interaction.user.id)
    if not member:
        return False
    
    return member.guild_permissions.manage_guild

async def require_admin(interaction: discord.Interaction) -> bool:
    """
    Check admin permissions and respond if lacking
    Returns True if admin, False otherwise
    """
    if not has_admin_permissions(interaction):
        embed = discord.Embed(
            title="Permission Denied",
            description="You need the **Manage Server** permission to use this command.",
            color=0xe74c3c
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return False
    return True

def validate_positive_integer(value: int, max_value: Optional[int] = None) -> bool:
    """Validate that a value is a positive integer within range"""
    if value < 1:
        return False
    if max_value and value > max_value:
        return False
    return True
