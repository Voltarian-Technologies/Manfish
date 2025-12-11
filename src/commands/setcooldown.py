"""
/setcooldown command - Admin command to adjust cooldowns
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.validation import require_admin, validate_positive_integer
from src.lib.config import update_settings_config, get_settings_config

class SetCooldown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setcooldown", description="[ADMIN] Set cooldown time for an activity")
    @app_commands.describe(category="The activity to set the cooldown for")
    @app_commands.describe(seconds="Cooldown in seconds (1-3600)")
    @app_commands.choices(category=[
        app_commands.Choice(name="Fishing", value="fish"),
        app_commands.Choice(name="Woodcutting", value="chop")
    ])
    async def setcooldown(self, interaction: discord.Interaction, category: app_commands.Choice[str], seconds: int):
        """Set cooldown admin command"""
        if not await require_admin(interaction):
            return
        
        # Validate input
        if not validate_positive_integer(seconds, 3600):
            embed = discord.Embed(
                title="Invalid Value",
                description="Cooldown must be between 1 and 3600 seconds (1 hour)",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Update settings
        settings = get_settings_config()
        cooldown_key = f"{category.value}Cooldown" # e.g., "fishCooldown" or "chopCooldown"
        settings[cooldown_key] = seconds
        success = update_settings_config(settings)
        
        if success:
            embed = discord.Embed(
                title="<:confirm:1444147698386079875> Cooldown Updated",
                description=f"**{category.name}** cooldown set to **{seconds}** seconds",
                color=0x2ecc71
            )
        else:
            embed = discord.Embed(
                title="<:deny:1444147699699023954> Error",
                description="Failed to save settings",
                color=0xe74c3c
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetCooldown(bot))
