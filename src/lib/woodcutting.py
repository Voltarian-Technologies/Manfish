"""
Woodcutting mechanics: RNG, cooldowns, harvest calculations
"""

import random
import time
from typing import Dict, Tuple, Optional
from .config import get_rates_config, get_settings_config, get_wood_cooldown, get_timber_bite_chance

# Log types by rarity
LOG_TYPES = {
    'Common': ['oak', 'birch'],
    'Uncommon': ['maple', 'ash'],
    'Rare': ['spruce', 'pine'],
    'Epic': ['bloodwood', 'honeywood'],
    'Legendary': ['shadowbark'],
    'Mythic': ['eternal']
}

# Base values per rarity
BASE_VALUES = {
    'Common': 10,
    'Uncommon': 30,
    'Rare': 75,
    'Epic': 200,
    'Legendary': 500,
    'Mythic': 1500
}

# Log multipliers within rarity
LOG_MULTIPLIERS = {
    'oak': 1.0,
    'birch': 0.8,
    'maple': 1.2,
    'ashwood': 1.0,
    'spruce': 1.5,
    'pine': 1.3,
    'bloodwood': 1.0,
    'honeywood': 1.0,
    'shadowbark': 1.0,
    'angelwood': 1.0
}

def check_cooldown(last_chop_timestamp: int) -> Tuple[bool, int]:
    """
    Check if user is on cooldown
    Returns (can_chop, remaining_seconds)
    """
    cooldown = get_wood_cooldown()
    current_time = int(time.time())
    time_passed = current_time - last_chop_timestamp
    
    if time_passed >= cooldown:
        return True, 0
    
    remaining = cooldown - time_passed
    return False, remaining

def get_harvest_weights(axe_tier: str, blade_sharpness: int, handle_strength: int) -> Dict[str, float]:
    """
    Get weighted probabilities for each rarity based on axe and upgrades
    """
    rates_config = get_rates_config()
    axe_rates = rates_config.get('axeTiers', {}).get(axe_tier, {})
    base_weights = axe_rates.get('weights', {
        'Common': 50,
        'Uncommon': 30,
        'Rare': 15,
        'Epic': 4,
        'Legendary': 0.9,
        'Mythic': 0.1
    })
    
    # Apply upgrade bonuses
    weights = base_weights.copy()
    
    # Blade sharpness increases rare+ chances
    rare_boost = 1 + (blade_sharpness * 0.05)
    weights['Rare'] *= rare_boost
    weights['Epic'] *= rare_boost
    weights['Legendary'] *= rare_boost
    weights['Mythic'] *= rare_boost
    
    # Handle strength increases epic+ chances
    epic_boost = 1 + (handle_strength * 0.03)
    weights['Epic'] *= epic_boost
    weights['Legendary'] *= epic_boost
    weights['Mythic'] *= epic_boost
    
    return weights

def roll_harvest(axe_tier: str, blade_sharpness: int, handle_strength: int) -> Tuple[str, str]:
    """
    Roll for a harvest
    Returns (rarity, log_type)
    """
    weights = get_harvest_weights(axe_tier, blade_sharpness, handle_strength)
    
    # Weighted random selection
    rarities = list(weights.keys())
    weight_values = list(weights.values())
    
    rarity = random.choices(rarities, weights=weight_values)[0]
    log_type = random.choice(LOG_TYPES[rarity])
    
    return rarity, log_type

def calculate_log_value(rarity: str, log_type: str, is_timber_bite: bool = False) -> int:
    """
    Calculate the value of a harvested log
    """
    base_value = BASE_VALUES[rarity]
    multiplier = LOG_MULTIPLIERS.get(log_type, 1.0)
    value = int(base_value * multiplier)
    
    if is_timber_bite:
        value *= 2
    
    return value

def check_timber_bite() -> bool:
    """
    Check if timber bite event triggers
    """
    chance = get_timber_bite_chance()
    return random.random() < chance

def attempt_chop(user_data: Dict) -> Dict:
    """
    Perform a chopping attempt
    Returns result dict with harvest info
    """
    # Check cooldown
    can_chop, remaining = check_cooldown(user_data['stats']['lastChopTimestamp'])
    
    if not can_chop:
        return {
            'success': False,
            'on_cooldown': True,
            'remaining_seconds': remaining
        }
    
    # Get user stats
    axe_tier = user_data['axe']['tier']
    blade_sharpness = user_data['upgrades'].get('bladeSharpness', 0)
    handle_strength = user_data['upgrades'].get('handleStrength', 0)
    
    # Roll for harvest
    rarity, log_type = roll_harvest(axe_tier, blade_sharpness, handle_strength)
    
    # Check for timber bite
    is_timber_bite = check_timber_bite()
    
    # Calculate value
    value = calculate_log_value(rarity, log_type, is_timber_bite)
    
    # Update user data
    user_data['stats']['totalChops'] += 1
    user_data['stats']['lastChopTimestamp'] = int(time.time())
    user_data['currency'] += value
    
    # Add to inventory
    if 'woodcutting' not in user_data['inventory']:
        user_data['inventory']['woodcutting'] = {}
    
    if rarity not in user_data['inventory']['woodcutting']:
        user_data['inventory']['woodcutting'][rarity] = {}
    
    if log_type not in user_data['inventory']['woodcutting'][rarity]:
        user_data['inventory']['woodcutting'][rarity][log_type] = 0
    
    user_data['inventory']['woodcutting'][rarity][log_type] += 1
    
    return {
        'success': True,
        'on_cooldown': False,
        'rarity': rarity,
        'log_type': log_type,
        'value': value,
        'is_timber_bite': is_timber_bite
    }
