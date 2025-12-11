"""
/chop command - Harvest logs with cooldown
"""

import discord
from discord import app_commands
from discord.ext import commands
from src.lib.persistence import load_user_data, save_user_data
from src.lib.woodcutting import attempt_chop
from src.lib.emojis import get_log_emoji, get_axe_emoji, get_rarity_color, format_currency

class Chop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="chop", description="Swing your axe and harvest logs!")
    async def chop(self, interaction: discord.Interaction):
        """Chop command"""
        await interaction.response.defer()
        try:
            user_id = interaction.user.id
            username = interaction.user.display_name
            
            # Load user data
            user_data = await load_user_data(user_id, username)
            
            # Ensure lastChopTimestamp exists for new users
            user_data.setdefault('lastChopTimestamp', 0)
            
            # Attempt to chop
            result = attempt_chop(user_data)
            
            if not result['success']:
                # On cooldown
                remaining = result['remaining_seconds']
                minutes = remaining // 60
                seconds = remaining % 60
                
                embed = discord.Embed(
                    title="<:deny:1444147699699023954> On Cooldown",
                    description=f"Your axe needs a rest!\nTry again in **{minutes}m {seconds}s**",
                    color=0x95a5a6
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return
            
            # Successful harvest
            rarity = result['rarity']
            log_type = result['log_type']
            value = result['value']
            is_timber = result['is_timber_bite']
            
            # Get emojis (with case-insensitive lookup for axe)
            axe_tier = user_data['axe']['tier']
            axe_emoji = get_axe_emoji(axe_tier.lower())
            log_emoji = get_log_emoji(log_type, rarity)
            
            # Build description
            title = "<:confirm:1444147698386079875> Woodcutting Success!"
            if is_timber:
                title = "<:plus:1444147702005891153> TIMBER BITE! <:plus:1444147702005891153>"
            
            description = f"You swing your {axe_emoji} **{axe_tier.title()}** and harvested:\n\n"
            description += f"{log_emoji} **{log_type.title()}** ({rarity})\n"
            description += f"{format_currency(value)}"
            
            if is_timber:
                description += "\n\n*Timber Bite doubled your reward!*"
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=get_rarity_color(rarity)
            )
            
            # Add stats footer
            embed.set_footer(text=f"Total chops: {user_data['stats']['totalChops']} | Balance: {user_data['currency']:,}")
            
            # Save user data
            await save_user_data(user_id, user_data)
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error in /chop command: {e}")
            await interaction.followup.send("<:deny:1444147699699023954> An error occurred while trying to chop. Please try again later.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Chop(bot))
