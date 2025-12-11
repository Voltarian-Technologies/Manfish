"""
/shop command - Display available upgrades
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data
from src.lib.economy import get_shop_items, get_upgrade_cost
from src.lib.emojis import format_currency

# Woodcutting upgrades
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

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="shop", description="View available upgrades in the shop")
    @app_commands.describe(category="The category of shop to view")
    @app_commands.choices(category=[
        app_commands.Choice(name="Fishing", value="fishing"),
        app_commands.Choice(name="Woodcutting", value="woodcutting"),
    ])
    async def shop(self, interaction: discord.Interaction, category: app_commands.Choice[str] = None):
        """Shop command"""
        user_id = interaction.user.id
        username = interaction.user.display_name
        
        user_data = await load_user_data(user_id, username)
        
        # Default to fishing if no category is provided
        shop_category = category.value if category else "fishing"

        if shop_category == "fishing":
            shop_items = get_shop_items()
            embed = discord.Embed(
                title="Fishing Shop",
                description="Purchase passive upgrades to improve your fishing!\nUse `/buy <upgrade>` to purchase.",
                color=0x9b59b6
            )
        else: # Woodcutting
            shop_items = woodcutting_shop_items
            embed = discord.Embed(
                title="Woodcutting Shop",
                description="Purchase passive upgrades to improve your woodcutting!\nUse `/buy <upgrade>` to purchase.",
                color=0xe67e22
            )

        # Add each upgrade
        for upgrade_key, item_info in shop_items.items():
            current_level = user_data['upgrades'].get(upgrade_key, 0)
            next_cost = get_upgrade_cost(upgrade_key, current_level)
            
            if next_cost is None:
                status = f"**MAX LEVEL** ({current_level}/{item_info['max_level']})"
            else:
                status = f"Level {current_level}/{item_info['max_level']}\nNext: {format_currency(next_cost)}"
            
            embed.add_field(
                name=f"{item_info['name']}",
                value=f"{item_info['description']}\n{status}",
                inline=False
            )
        
        embed.set_footer(text=f"Your balance: {user_data['currency']:,} Chum")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))
