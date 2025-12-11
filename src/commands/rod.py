"""
/rod command - Show current rod and upgrade info
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data
from src.lib.economy import get_next_rod_tier
from src.lib.emojis import get_rod_emoji, format_currency

class Rod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="rod", description="View your current fishing rod")
    async def rod(self, interaction: discord.Interaction):
        """Rod command"""
        user_id = interaction.user.id
        username = interaction.user.display_name
        
        user_data = await load_user_data(user_id, username)
        
        current_tier = user_data['rod']['tier']
        rod_emoji = get_rod_emoji(current_tier)
        
        embed = discord.Embed(
            title=f"{username}'s Fishing Rod",
            description=f"{rod_emoji} **{current_tier} Rod**",
            color=0x3498db
        )
        
        # Check for next upgrade
        next_tier, cost = get_next_rod_tier(current_tier)
        
        if next_tier:
            next_emoji = get_rod_emoji(next_tier)
            embed.add_field(
                name="Next Upgrade",
                value=f"{next_emoji} **{next_tier} Rod**\nCost: {format_currency(cost)}",
                inline=False
            )
            embed.set_footer(text="Use /upgrade item:Rod to buy the next rod tier")
        else:
            embed.add_field(
                name="Max Tier Reached",
                value="You have the best rod available!",
                inline=False
            )
        
        # Add upgrade info
        hook = user_data['upgrades'].get('hookSharpness', 0)
        line = user_data['upgrades'].get('lineStrength', 0)
        
        embed.add_field(
            name="Passive Upgrades",
            value=f"Hook Sharpness: Level {hook}\nLine Strength: Level {line}",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Rod(bot))
