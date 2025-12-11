"""
/fish command - Catch fish with cooldown
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data, save_user_data
from src.lib.fishing import attempt_fish
from src.lib.emojis import get_fish_emoji, get_rod_emoji, get_rarity_color, format_currency

class Fish(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="fish", description="Cast your rod and catch a fish!")
    async def fish(self, interaction: discord.Interaction):
        """Fish command"""
        await interaction.response.defer()
        try:
            user_id = interaction.user.id
            username = interaction.user.display_name
            
            # Load user data
            user_data = await load_user_data(user_id, username)
            
            # Ensure lastFishTimestamp exists for new users
            user_data.setdefault('lastFishTimestamp', 0)
            
            # Attempt to fish
            result = attempt_fish(user_data)
            
            if not result['success']:
                # On cooldown
                remaining = result['remaining_seconds']
                minutes = remaining // 60
                seconds = remaining % 60
                
                embed = discord.Embed(
                    title="<:deny:1444147699699023954> On Cooldown",
                    description=f"Your fishing rod needs a rest!\nTry again in **{minutes}m {seconds}s**",
                    color=0x95a5a6
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            # Successful catch
            rarity = result['rarity']
            fish_type = result['fish_type']
            value = result['value']
            is_golden = result['is_golden_bite']
            
            # Get emojis
            rod_emoji = get_rod_emoji(user_data['rod']['tier'])
            fish_emoji = get_fish_emoji(fish_type, rarity)
            
            # Build description
            title = "<:confirm:1444147698386079875> Fishing Success!"
            if is_golden:
                title = "<:plus:1444147702005891153> GOLDEN BITE! <:plus:1444147702005891153>"
            
            description = f"You cast your {rod_emoji} **{user_data['rod']['tier']}** and caught:\n\n"
            description += f"{fish_emoji} **{fish_type.title()}** ({rarity})\n"
            description += f"{format_currency(value)}"
            
            if is_golden:
                description += "\n\n*Golden Bite doubled your reward!*"
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=get_rarity_color(rarity)
            )
            
            # Add stats footer
            embed.set_footer(text=f"Total catches: {user_data['stats']['totalCatches']} | Balance: {user_data['currency']:,}")
            
            # Save user data
            await save_user_data(user_id, user_data)
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error in /fish command: {e}")
            await interaction.followup.send("<:deny:1444147699699023954> An error occurred while trying to fish. Please try again later.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Fish(bot))
