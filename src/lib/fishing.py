"""
Fishing mechanics: RNG, cooldowns, catch calculations
"""

import random
import time
from typing import Dict, Tuple, Optional
from .config import get_rates_config, get_settings_config, get_fish_cooldown, get_golden_bite_chance

# Fish types by rarity
FISH_TYPES = {
    'Common': ['cod', 'herring'],
    'Uncommon': ['trout', 'bass'],
    'Rare': ['shrimp', 'puffer'],
    'Epic': ['bloodborn','candy'],
    'Legendary': ['spookster'],
    'Mythic': ['priceless']
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

# Fish multipliers within rarity
FISH_MULTIPLIERS = {
    'cod': 1.0,
    'herring': 0.8,
    'trout': 1.2,
    'bass': 1.0,
    'shrimp': 1.5,
    'puffer': 1.3,
    'swordfish': 1.0,
    'spookster': 1.0,
    'priceless': 1.0
}

def check_cooldown(last_fish_timestamp: int) -> Tuple[bool, int]:
    """
    Check if user is on cooldown
    Returns (can_fish, remaining_seconds)
    """
    cooldown = get_fish_cooldown()
    current_time = int(time.time())
    time_passed = current_time - last_fish_timestamp
    
    if time_passed >= cooldown:
        return True, 0
    
    remaining = cooldown - time_passed
    return False, remaining

def get_catch_weights(rod_tier: str, hook_sharpness: int, line_strength: int) -> Dict[str, float]:
    """
    Get weighted probabilities for each rarity based on rod and upgrades
    """
    rates_config = get_rates_config()
    rod_rates = rates_config.get('rodTiers', {}).get(rod_tier, {})
    base_weights = rod_rates.get('weights', {
        'Common': 50,
        'Uncommon': 30,
        'Rare': 15,
        'Epic': 4,
        'Legendary': 0.9,
        'Mythic': 0.1
    })
    
    # Apply upgrade bonuses
    weights = base_weights.copy()
    
    # Hook sharpness increases rare+ chances
    rare_boost = 1 + (hook_sharpness * 0.05)
    weights['Rare'] *= rare_boost
    weights['Epic'] *= rare_boost
    weights['Legendary'] *= rare_boost
    weights['Mythic'] *= rare_boost
    
    # Line strength increases epic+ chances
    epic_boost = 1 + (line_strength * 0.03)
    weights['Epic'] *= epic_boost
    weights['Legendary'] *= epic_boost
    weights['Mythic'] *= epic_boost
    
    return weights

def roll_catch(rod_tier: str, hook_sharpness: int, line_strength: int) -> Tuple[str, str]:
    """
    Roll for a catch
    Returns (rarity, fish_type)
    """
    weights = get_catch_weights(rod_tier, hook_sharpness, line_strength)
    
    # Weighted random selection
    rarities = list(weights.keys())
    weight_values = list(weights.values())
    
    rarity = random.choices(rarities, weights=weight_values)[0]
    fish_type = random.choice(FISH_TYPES[rarity])
    
    return rarity, fish_type

def calculate_fish_value(rarity: str, fish_type: str, is_golden_bite: bool = False) -> int:
    """
    Calculate the value of a caught fish
    """
    base_value = BASE_VALUES[rarity]
    multiplier = FISH_MULTIPLIERS.get(fish_type, 1.0)
    value = int(base_value * multiplier)
    
    if is_golden_bite:
        value *= 2
    
    return value

def check_golden_bite() -> bool:
    """
    Check if golden bite event triggers
    """
    chance = get_golden_bite_chance()
    return random.random() < chance

def attempt_fish(user_data: Dict) -> Dict:
    """
    Perform a fishing attempt
    Returns result dict with catch info
    """
    # Check cooldown
    can_fish, remaining = check_cooldown(user_data['stats']['lastFishTimestamp'])
    
    if not can_fish:
        return {
            'success': False,
            'on_cooldown': True,
            'remaining_seconds': remaining
        }
    
    # Get user stats
    rod_tier = user_data['rod']['tier']
    hook_sharpness = user_data['upgrades'].get('hookSharpness', 0)
    line_strength = user_data['upgrades'].get('lineStrength', 0)
    
    # Roll for catch
    rarity, fish_type = roll_catch(rod_tier, hook_sharpness, line_strength)
    
    # Check for golden bite
    is_golden_bite = check_golden_bite()
    
    # Calculate value
    value = calculate_fish_value(rarity, fish_type, is_golden_bite)
    
    # Update user data
    user_data['stats']['totalCatches'] += 1
    user_data['stats']['lastFishTimestamp'] = int(time.time())
    user_data['currency'] += value
    
    # Add to inventory
    if fish_type not in user_data['inventory'][rarity]:
        user_data['inventory'][rarity][fish_type] = 0
    user_data['inventory'][rarity][fish_type] += 1
    
    return {
        'success': True,
        'on_cooldown': False,
        'rarity': rarity,
        'fish_type': fish_type,
        'value': value,
        'is_golden_bite': is_golden_bite
    }
