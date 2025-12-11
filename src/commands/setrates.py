"""
/setrates command - Admin command to adjust catch rates
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.validation import require_admin
from src.lib.config import update_rates_config, get_rates_config

class SetRates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setrates", description="[ADMIN] Adjust catch rate weights")
    @app_commands.describe(
        rod_tier="Rod tier to modify",
        rarity="Rarity to adjust",
        weight="New weight value (higher = more common)"
    )
    async def setrates(
        self,
        interaction: discord.Interaction,
        rod_tier: str,
        rarity: str,
        weight: float
    ):
        """Set rates admin command"""
        if not await require_admin(interaction):
            return
        
        # Validate weight
        if weight < 0:
            embed = discord.Embed(
                title="Invalid Weight",
                description="Weight must be a positive number",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Update rates
        rates = get_rates_config()
        
        if 'rodTiers' not in rates:
            rates['rodTiers'] = {}
        if rod_tier not in rates['rodTiers']:
            rates['rodTiers'][rod_tier] = {'weights': {}}
        if 'weights' not in rates['rodTiers'][rod_tier]:
            rates['rodTiers'][rod_tier]['weights'] = {}
        
        rates['rodTiers'][rod_tier]['weights'][rarity] = weight
        
        success = update_rates_config(rates)
        
        if success:
            embed = discord.Embed(
                title="<:confirm:1444147698386079875> Rates Updated",
                description=f"Set {rarity} weight to **{weight}** for {rod_tier} rod",
                color=0x2ecc71
            )
        else:
            embed = discord.Embed(
                title="<:deny:1444147699699023954> Error",
                description="Failed to save rate configuration",
                color=0xe74c3c
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetRates(bot))
