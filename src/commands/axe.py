"""
/axe command - Show current axe and upgrade info
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data
from src.lib.economy import get_next_axe_tier
from src.lib.emojis import get_axe_emoji, format_currency

class Axe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="axe", description="View your current woodcutting axe")
    async def axe(self, interaction: discord.Interaction):
        """Axe command"""
        user_id = interaction.user.id
        username = interaction.user.display_name
        
        user_data = await load_user_data(user_id, username)
        
        current_tier = user_data['axe']['tier']
        axe_emoji = get_axe_emoji(current_tier)
        
        embed = discord.Embed(
            title=f"{username}'s Woodcutting Axe",
            description=f"{axe_emoji} **{current_tier.title()}**",
            color=0xe67e22
        )
        
        # Check for next upgrade
        next_tier, cost = get_next_axe_tier(current_tier)
        
        if next_tier:
            next_emoji = get_axe_emoji(next_tier)
            embed.add_field(
                name="Next Upgrade",
                value=f"{next_emoji} **{next_tier.title()}**\nCost: {format_currency(cost)}",
                inline=False
            )
            embed.set_footer(text="Use /upgrade item:Axe to buy the next axe tier")
        else:
            embed.add_field(
                name="Max Tier Reached",
                value="You have the best axe available!",
                inline=False
            )
        
        # Add upgrade info
        blade = user_data['upgrades'].get('bladeSharpness', 0)
        handle = user_data['upgrades'].get('handleStrength', 0)
        
        embed.add_field(
            name="Passive Upgrades",
            value=f"Blade Sharpness: Level {blade}\nHandle Strength: Level {handle}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Axe(bot))
