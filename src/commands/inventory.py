"""
/inventory command - View fish inventory
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data
from src.lib.economy import calculate_inventory_value
from src.lib.emojis import get_fish_emoji, get_rarity_color

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="inventory", description="View your fish inventory")
    async def inventory(self, interaction: discord.Interaction):
        """Inventory command"""
        user_id = interaction.user.id
        username = interaction.user.display_name
        
        user_data = await load_user_data(user_id, username)
        inventory = user_data['inventory']
        
        # Calculate total value
        total_value = calculate_inventory_value(inventory)
        
        embed = discord.Embed(
            title=f"<:inventory:1444147700902920302> {username}'s Inventory",
            description=f"Total estimated value: **{total_value:,}** Chum",
            color=0x3498db
        )
        
        # Add fish by rarity
        has_fish = False
        for rarity in ['Mythic', 'Legendary', 'Epic', 'Rare', 'Uncommon', 'Common']:
            if rarity in inventory and inventory[rarity]:
                fish_list = []
                for fish_type, count in inventory[rarity].items():
                    if count > 0:
                        emoji = get_fish_emoji(fish_type, rarity)
                        fish_list.append(f"{emoji} {fish_type.title()}: **{count}**")
                        has_fish = True
                
                if fish_list:
                    embed.add_field(
                        name=f"{rarity} Fish",
                        value="\n".join(fish_list),
                        inline=False
                    )
        
        if not has_fish:
            embed.description = "Your inventory is empty. Go fishing with `/fish`!"
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Inventory(bot))
