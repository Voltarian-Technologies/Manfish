"""
/buy command - Purchase upgrades from shop
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data, save_user_data
from src.lib.economy import get_shop_items, get_upgrade_cost
from src.lib.emojis import format_currency

# Woodcutting upgrades (from shop.py)
woodcutting_shop_items = {
    'bladeSharpness': {
        'name': 'Blade Sharpness',
        'description': 'Increases your chance of finding rare logs.',
        'max_level': 10
    },
    'handleStrength': {
        'name': 'Handle Strength',
        'description': 'Increases your chance of getting a "Timber Bite" (double reward).',
        'max_level': 5
    }
}

class Buy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="buy", description="Purchase an upgrade from the shop")
    @app_commands.describe(upgrade="The upgrade to purchase (e.g. hooksharpness, bladesharpness)")
    async def buy(self, interaction: discord.Interaction, upgrade: str):
        """Buy command"""
        user_id = interaction.user.id
        username = interaction.user.display_name
        
        user_data = await load_user_data(user_id, username)
        
        # Normalize upgrade name
        upgrade = upgrade.lower().replace(' ', '').replace('_', '').replace('-', '')
        
        # Map to actual upgrade key
        upgrade_map = {
            'hooksharpness': 'hookSharpness',
            'linestrength': 'lineStrength',
            'bladesharpness': 'bladeSharpness',
            'handlestrength': 'handleStrength'
        }
        
        upgrade_key = upgrade_map.get(upgrade)
        
        # Combine all shop items
        all_shop_items = get_shop_items()
        all_shop_items.update(woodcutting_shop_items)
        
        if not upgrade_key or upgrade_key not in all_shop_items:
            valid_upgrades = ", ".join([f"`{k}`" for k in upgrade_map.keys()])
            embed = discord.Embed(
                title="<:deny:1444147699699023954> Invalid Upgrade",
                description=f"Please choose a valid upgrade.\nUse `/shop` to see available upgrades.",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Get upgrade info
        item_info = all_shop_items[upgrade_key]
        current_level = user_data['upgrades'].get(upgrade_key, 0)
        cost = get_upgrade_cost(upgrade_key, current_level)
        
        if cost is None:
            embed = discord.Embed(
                title="Max Level Reached",
                description=f"Your {item_info['name']} is already at maximum level!",
                color=0x95a5a6
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if user can afford
        if user_data['currency'] < cost:
            embed = discord.Embed(
                title="<:deny:1444147699699023954> Insufficient Funds",
                description=f"You need {format_currency(cost)} to upgrade {item_info['name']}.\nYour balance: {format_currency(user_data['currency'])}",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Perform purchase
        user_data['currency'] -= cost
        user_data['upgrades'].setdefault(upgrade_key, 0)
        user_data['upgrades'][upgrade_key] += 1
        
        await save_user_data(user_id, user_data)
        
        # Success message
        new_level = current_level + 1
        embed = discord.Embed(
            title="<:confirm:1444147698386079875> Upgrade Purchased!",
            description=f"**{item_info['name']}** upgraded to Level {new_level}!",
            color=0x2ecc71
        )
        embed.add_field(
            name="Effect",
            value=item_info['description'],
            inline=False
        )
        embed.add_field(
            name="New Balance",
            value=format_currency(user_data['currency']),
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Buy(bot))
