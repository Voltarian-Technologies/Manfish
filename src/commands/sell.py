"""
/sell command - Sell items from your inventory
"""

import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

from src.lib.persistence import load_user_data, save_user_data
from src.lib.config import get_costs_config
from src.lib.emojis import format_currency

class Sell(commands.GroupCog, name="sell"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.costs = get_costs_config()
        super().__init__()

    async def _sell_items(self, interaction: discord.Interaction, item_category: str, item_type: Optional[str], amount: Optional[int]):
        """Generic function to sell items."""
        await interaction.response.defer()

        user_id = interaction.user.id
        username = interaction.user.display_name
        user_data = await load_user_data(user_id, username)

        inventory_key = f"{item_category}" # "logs" or "fish"
        values_key = f"{item_category}Values" # "logValues" or "fishValues"

        if inventory_key not in user_data.get('inventory', {}):
            user_data['inventory'][inventory_key] = {}

        inventory = user_data['inventory'][inventory_key]
        item_values = self.costs[values_key]

        items_to_sell = {}
        
        # Determine which items and amounts to sell
        if item_type:
            # Selling a specific type of item
            item_type = item_type.lower()
            if item_type not in inventory or inventory[item_type] == 0:
                await interaction.followup.send(f"You don't have any **{item_type.title()}** to sell.", ephemeral=True)
                return
            
            amount_to_sell = inventory[item_type] if amount is None else amount
            if amount_to_sell > inventory[item_type]:
                await interaction.followup.send(f"You only have **{inventory[item_type]}** {item_type.title()} to sell.", ephemeral=True)
                return
            
            items_to_sell[item_type] = amount_to_sell
        else:
            # Selling all items in the category
            if not inventory:
                await interaction.followup.send(f"You don't have any {inventory_key} to sell.", ephemeral=True)
                return
            for i_type, i_amount in inventory.items():
                if i_amount > 0:
                    items_to_sell[i_type] = i_amount

        if not items_to_sell:
            await interaction.followup.send(f"You don't have any {inventory_key} to sell.", ephemeral=True)
            return

        # Calculate total value and update inventory
        total_value = 0
        sold_description = []
        for i_type, i_amount in items_to_sell.items():
            value = item_values.get(i_type, 0) * i_amount
            total_value += value
            inventory[i_type] -= i_amount
            sold_description.append(f"**{i_amount}** {i_type.title()} for {format_currency(value)}")

        user_data['currency'] += total_value
        await save_user_data(user_id, user_data)

        embed = discord.Embed(
            title="<:confirm:1444147698386079875> Items Sold!",
            description="\n".join(sold_description),
            color=0x2ecc71
        )
        embed.add_field(name="Total Earnings", value=format_currency(total_value))
        embed.set_footer(text=f"New Balance: {format_currency(user_data['currency'])}")

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="logs", description="Sell your harvested logs.")
    @app_commands.describe(
        item_type="The type of log to sell (e.g., oak). Sells all logs if omitted.",
        amount="The amount to sell. Sells all of that type if omitted."
    )
    async def sell_logs(self, interaction: discord.Interaction, item_type: Optional[str] = None, amount: Optional[app_commands.Range[int, 1]] = None):
        await self._sell_items(interaction, "logs", item_type, amount)

    @sell_logs.autocomplete('item_type')
    async def logs_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        log_types = list(self.costs['logValues'].keys())
        return [
            app_commands.Choice(name=log.title(), value=log)
            for log in log_types if current.lower() in log.lower()
        ][:25]

    @app_commands.command(name="fish", description="Sell your caught fish.")
    @app_commands.describe(
        item_type="The type of fish to sell (e.g., cod). Sells all fish if omitted.",
        amount="The amount to sell. Sells all of that type if omitted."
    )
    async def sell_fish(self, interaction: discord.Interaction, item_type: Optional[str] = None, amount: Optional[app_commands.Range[int, 1]] = None):
        await self._sell_items(interaction, "fish", item_type, amount)

    @sell_fish.autocomplete('item_type')
    async def fish_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        fish_types = list(self.costs['fishValues'].keys())
        return [
            app_commands.Choice(name=fish.title(), value=fish)
            for fish in fish_types if current.lower() in fish.lower()
        ][:25]

async def setup(bot: commands.Bot):
    await bot.add_cog(Sell(bot))