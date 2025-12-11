"""
/balance command - Show user's currency
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data
from src.lib.emojis import format_currency

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="balance", description="Check your currency balance")
    async def balance(self, interaction: discord.Interaction):
        """Balance command"""
        user_id = interaction.user.id
        username = interaction.user.display_name
        
        user_data = await load_user_data(user_id, username)
        
        embed = discord.Embed(
            title=f"<:chum_bucket:1444145395214323764> {username}'s Balance",
            description=format_currency(user_data['currency']),
            color=0xf39c12
        )
        
        # Add stats
        embed.add_field(
            name="Total Catches",
            value=f"{user_data['stats']['totalCatches']:,}",
            inline=True
        )
        embed.add_field(
            name="Current Rod",
            value=user_data['rod']['tier'],
            inline=True
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Balance(bot))
