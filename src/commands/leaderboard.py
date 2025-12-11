"""
/leaderboard command - Show rankings
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal
from src.lib.leaderboards import get_richest_leaderboard, get_catches_leaderboard, get_rod_leaderboard
from src.lib.emojis import format_currency, get_rod_emoji

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="leaderboard", description="View server leaderboards")
    @app_commands.describe(category="Leaderboard category to view")
    async def leaderboard(
        self,
        interaction: discord.Interaction,
        category: Literal["richest", "catches", "rods"] = "richest"
    ):
        """Leaderboard command"""
        
        await interaction.response.defer()
        
        if category == "richest":
            data = await get_richest_leaderboard()
            title = "<:chum_bucket:1444145395214323764> Richest Players"
            
            description = ""
            for i, (username, user_id, currency) in enumerate(data, 1):
                medal = "<:profile:1444147703067181237>" if i == 1 else "<:profile:1444147703067181237>" if i == 2 else "<:profile:1444147703067181237>" if i == 3 else f"**{i}.**"
                description += f"{medal} {username}: {format_currency(currency)}\n"
            
        elif category == "catches":
            data = await get_catches_leaderboard()
            title = "<:inventory:1444147700902920302> Most Catches"
            
            description = ""
            for i, (username, user_id, catches) in enumerate(data, 1):
                medal = "<:profile:1444147703067181237>" if i == 1 else "<:profile:1444147703067181237>" if i == 2 else "<:profile:1444147703067181237>" if i == 3 else f"**{i}.**"
                description += f"{medal} {username}: **{catches:,}** fish\n"
            
        else:  # rods
            data = await get_rod_leaderboard()
            title = "<:rod_of_the_sea:1443784013167984711> Best Rods"
            
            description = ""
            for i, (username, user_id, rod_tier, tier_index) in enumerate(data, 1):
                medal = "<:profile:1444147703067181237>" if i == 1 else "<:profile:1444147703067181237>" if i == 2 else "<:profile:1444147703067181237>" if i == 3 else f"**{i}.**"
                rod_emoji = get_rod_emoji(rod_tier)
                description += f"{medal} {username}: {rod_emoji} {rod_tier}\n"
        
        if not description:
            description = "No data available yet. Start fishing!"
        
        embed = discord.Embed(
            title=title,
            description=description,
            color=0xf39c12
        )
        embed.set_footer(text="Keep fishing to climb the ranks!")
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
