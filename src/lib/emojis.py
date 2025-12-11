"""
Emoji resolution and formatting utilities
"""

from typing import Optional
from .config import get_emoji_config

def get_emoji(category: str, name: str) -> str:
    """
    Get an emoji string from the config
    Returns the emoji or a fallback text
    """
    config = get_emoji_config()
    
    if category in config and name in config[category]:
        emoji_value = config[category][name]
        
        # Handle custom emoji format <:name:id> or <a:name:id>
        if isinstance(emoji_value, str):
            if emoji_value.startswith('<') and emoji_value.endswith('>'):
                return emoji_value
            # If it's just text, return it
            return emoji_value
    
    # Fallback to text representation
    return f"[{name}]"

def get_fish_emoji(fish_type: str, rarity: str) -> str:
    """Get emoji for a specific fish"""
    return get_emoji('fish', f"{fish_type}_{rarity.lower()}")

def get_log_emoji(log_type: str, rarity: str) -> str:
    """Get emoji for a specific log"""
    return get_emoji('logs', f"{log_type}_{rarity.lower()}")

def get_rod_emoji(rod_tier: str) -> str:
    """Get emoji for a rod tier"""
    return get_emoji('rods', rod_tier.lower())

def get_axe_emoji(axe_tier: str) -> str:
    """Get emoji for an axe tier"""
    return get_emoji('axes', axe_tier.lower())

def get_rarity_color(rarity: str) -> int:
    """Get Discord embed color for a rarity tier"""
    colors = {
        'Common': 0x95a5a6,      # Gray
        'Uncommon': 0x2ecc71,    # Green
        'Rare': 0x3498db,        # Blue
        'Epic': 0x9b59b6,        # Purple
        'Legendary': 0xf39c12,   # Orange
        'Mythic': 0xe74c3c       # Red
    }
    return colors.get(rarity, 0x95a5a6)

def format_currency(amount: int) -> str:
    """Format currency with emoji"""
    currency_emoji = get_emoji('misc', 'currency')
    from .config import get_currency_name
    return f"{currency_emoji} {amount:,} {get_currency_name()}"
