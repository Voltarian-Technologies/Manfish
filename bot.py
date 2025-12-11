"""
Discord Fishing Bot - Main Entry Point
A feature-rich fishing bot with economy, upgrades, and leaderboards
"""

import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

from src.commands import fish, balance, sell, inventory, upgrade, rod, shop, buy, leaderboard
from src.commands import setemojis, setcooldown, setrates
from src.commands import chop, axe
from src.lib.config import load_all_configs

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables")

# Create bot instance with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load all configurations on startup
@bot.event
async def on_ready():
    """Bot startup event"""
    print(f'🎣 {bot.user} is now online!')
    print(f'📊 Connected to {len(bot.guilds)} guild(s)')
    
    # Load configurations
    try:
        load_all_configs()
        print('✅ Configurations loaded successfully')
    except Exception as e:
        print(f'⚠️ Error loading configurations: {e}')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} slash command(s)')
    except Exception as e:
        print(f'❌ Failed to sync commands: {e}')

@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore command not found errors
    
    print(f'Error in command {ctx.command}: {error}')
    await ctx.send(f'❌ An error occurred: {str(error)}')

# Register all commands
async def setup_commands():
    """Setup all bot commands"""
    # Player commands
    await bot.add_cog(fish.Fish(bot))
    await bot.add_cog(balance.Balance(bot))
    await bot.add_cog(sell.Sell(bot))
    await bot.add_cog(inventory.Inventory(bot))
    await bot.add_cog(upgrade.Upgrade(bot))
    await bot.add_cog(rod.Rod(bot))
    await bot.add_cog(chop.Chop(bot))
    await bot.add_cog(axe.Axe(bot))
    await bot.add_cog(shop.Shop(bot))
    await bot.add_cog(buy.Buy(bot))
    await bot.add_cog(leaderboard.Leaderboard(bot))
    
    # Admin commands
    await bot.add_cog(setemojis.SetEmojis(bot))
    await bot.add_cog(setcooldown.SetCooldown(bot))
    await bot.add_cog(setrates.SetRates(bot))

# Main execution
async def main():
    """Main async function to run the bot"""
    async with bot:
        await setup_commands()
        await bot.start(TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n👋 Bot shutting down...')
