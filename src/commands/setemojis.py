"""
/setemojis command - Admin command to set custom emojis
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.validation import require_admin
from src.lib.config import update_emoji_config, get_emoji_config

class SetEmojis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setemojis", description="[ADMIN] Configure custom emojis")
    @app_commands.describe(
        category="Category (fish, rods, misc)",
        name="Emoji name (e.g., salmon_common, wood)",
        emoji="The emoji to use (custom or unicode)"
    )
    async def setemojis(
        self,
        interaction: discord.Interaction,
        category: str,
        name: str,
        emoji: str
    ):
        """Set emojis admin command"""
        if not await require_admin(interaction):
            return
        
        # Get current config
        emoji_config = get_emoji_config()
        
        # Initialize category if needed
        if category not in emoji_config:
            emoji_config[category] = {}
        
        # Update emoji
        emoji_config[category][name] = emoji
        
        # Save config
        success = update_emoji_config(emoji_config)
        
        if success:
            embed = discord.Embed(
                title="<:confirm:1444147698386079875> Emoji Updated",
                description=f"Set `{category}.{name}` to {emoji}",
                color=0x2ecc71
            )
        else:
            embed = discord.Embed(
                title="<:deny:1444147699699023954> Error",
                description="Failed to save emoji configuration",
                color=0xe74c3c
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetEmojis(bot))
