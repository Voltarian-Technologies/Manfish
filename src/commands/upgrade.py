"""
/upgrade command - Upgrade to next rod or axe tier
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data, save_user_data
from src.lib.economy import get_next_rod_tier, get_next_axe_tier
from src.lib.emojis import get_rod_emoji, get_axe_emoji, format_currency

class Upgrade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="upgrade", description="Upgrade your fishing rod or woodcutting axe to the next tier")
    @app_commands.describe(item="The item you want to upgrade")
    @app_commands.choices(item=[
        app_commands.Choice(name="Rod", value="rod"),
        app_commands.Choice(name="Axe", value="axe"),
    ])
    async def upgrade(self, interaction: discord.Interaction, item: app_commands.Choice[str]):
        """Upgrade command"""
        user_id = interaction.user.id
        username = interaction.user.display_name
        
        user_data = await load_user_data(user_id, username)
        
        if item.value == "rod":
            await self.upgrade_rod(interaction, user_data)
        elif item.value == "axe":
            await self.upgrade_axe(interaction, user_data)

    async def upgrade_rod(self, interaction: discord.Interaction, user_data: dict):
        """Upgrade the fishing rod"""
        current_tier = user_data['rod']['tier']
        next_tier, cost = get_next_rod_tier(current_tier)
        
        if not next_tier:
            embed = discord.Embed(
                title="Max Tier Reached",
                description="You already have the best fishing rod available!",
                color=0x95a5a6
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if user can afford
        if user_data['currency'] < cost:
            embed = discord.Embed(
                title="<:deny:1444147699699023954> Insufficient Funds",
                description=f"You need {format_currency(cost)} to upgrade to the {next_tier} rod.\nYour balance: {format_currency(user_data['currency'])}",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Perform upgrade
        user_data['currency'] -= cost
        user_data['rod']['tier'] = next_tier
        user_data['rod']['level'] += 1
        
        await save_user_data(interaction.user.id, user_data)
        
        # Success message
        rod_emoji = get_rod_emoji(next_tier)
        embed = discord.Embed(
            title="<:plus:1444147702005891153> Rod Upgraded!",
            description=f"Upgraded to {rod_emoji} **{next_tier}**!",
            color=0x2ecc71
        )
        embed.add_field(name="Benefits", value="• Improved bite rate\n• Better catch chances\n• Increased Rare+ probabilities", inline=False)
        embed.add_field(name="New Balance", value=format_currency(user_data['currency']), inline=False)
        
        await interaction.response.send_message(embed=embed)

    async def upgrade_axe(self, interaction: discord.Interaction, user_data: dict):
        """Upgrade the woodcutting axe"""
        current_tier = user_data['axe']['tier']
        next_tier, cost = get_next_axe_tier(current_tier)
        
        if not next_tier:
            embed = discord.Embed(
                title="Max Tier Reached",
                description="You already have the best woodcutting axe available!",
                color=0x95a5a6
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if user can afford
        if user_data['currency'] < cost:
            embed = discord.Embed(
                title="<:deny:1444147699699023954> Insufficient Funds",
                description=f"You need {format_currency(cost)} to upgrade to the {next_tier.title()} axe.\nYour balance: {format_currency(user_data['currency'])}",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Perform upgrade
        user_data['currency'] -= cost
        user_data['axe']['tier'] = next_tier
        
        await save_user_data(interaction.user.id, user_data)
        
        # Success message
        axe_emoji = get_axe_emoji(next_tier)
        embed = discord.Embed(
            title="<:plus:1444147702005891153> Axe Upgraded!",
            description=f"Upgraded to {axe_emoji} **{next_tier.title()}**!",
            color=0x2ecc71
        )
        embed.add_field(name="Benefits", value="• Improved chop speed\n• Better log chances\n• Increased Rare+ probabilities", inline=False)
        embed.add_field(name="New Balance", value=format_currency(user_data['currency']), inline=False)
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Upgrade(bot))
