"""
Economy calculations: upgrades, prices, selling
"""

from typing import Dict, Tuple
from .fishing import BASE_VALUES as FISH_BASE_VALUES, FISH_MULTIPLIERS
from .woodcutting import BASE_VALUES as LOG_BASE_VALUES, LOG_MULTIPLIERS

# Rod tier progression
ROD_TIERS = ['Starter Rod', 'Speedster Rod', 'Challenge Rod', 'Legend Rod', 'Rod of The Sea', 'Yeti Rod', 'Bingo Rod', 'Bingo Rod Tier 2']

# Axe tier progression
AXE_TIERS = ['Starter Axe', 'Speedster Axe', 'Challenge Axe', 'Legend Axe', 'Axe of the Forest', 'Yeti Axe', 'Bingo Axe', 'Bingo Axe Tier 2']

# Rod upgrade costs (exponential)
ROD_COSTS = {
    'Speedster Rod': 500,
    'Challenge Rod': 2000,
    'Legend Rod': 8000,
    'Rod of The Sea': 30000,
    'Yeti Rod': 40000,
    'Bingo Rod': 60000,
    'Bingo Rod Tier 2': 100000
}

# Axe upgrade costs (exponential)
AXE_COSTS = {
    'Speedster Axe': 500,
    'Challenge Axe': 2000,
    'Legend Axe': 8000,
    'Axe of the Forest': 30000,
    'Yeti Axe': 40000,
    'Bingo Axe': 60000,
    'Bingo Axe Tier 2': 100000
}

# Passive upgrade costs
UPGRADE_COSTS = {
    'hookSharpness': lambda level: 300 * (2 ** level),
    'lineStrength': lambda level: 400 * (2 ** level),
    'bladeSharpness': lambda level: 300 * (2 ** level),
    'handleStrength': lambda level: 400 * (2 ** level)
}

UPGRADE_MAX_LEVEL = 10

def get_rod_tier_index(tier: str) -> int:
    """Get numeric index of rod tier"""
    try:
        return ROD_TIERS.index(tier)
    except ValueError:
        return 0

def get_axe_tier_index(tier: str) -> int:
    """Get numeric index of axe tier"""
    try:
        return AXE_TIERS.index(tier)
    except ValueError:
        return 0

def get_next_rod_tier(current_tier: str) -> Tuple[str | None, int | None]:
    """
    Get the next rod tier and its cost
    Returns (tier_name, cost) or (None, None) if max tier
    """
    current_index = get_rod_tier_index(current_tier)
    
    if current_index >= len(ROD_TIERS) - 1:
        return None, None
    
    next_tier = ROD_TIERS[current_index + 1]
    cost = ROD_COSTS.get(next_tier, 0)
    
    return next_tier, cost

def get_next_axe_tier(current_tier: str) -> Tuple[str | None, int | None]:
    """
    Get the next axe tier and its cost
    Returns (tier_name, cost) or (None, None) if max tier
    """
    current_index = get_axe_tier_index(current_tier)
    
    if current_index >= len(AXE_TIERS) - 1:
        return None, None
    
    next_tier = AXE_TIERS[current_index + 1]
    cost = AXE_COSTS.get(next_tier, 0)
    
    return next_tier, cost

def get_upgrade_cost(upgrade_type: str, current_level: int) -> int | None:
    """
    Get the cost for the next upgrade level
    Returns None if max level reached
    """
    if current_level >= UPGRADE_MAX_LEVEL:
        return None
    
    cost_func = UPGRADE_COSTS.get(upgrade_type)
    if not cost_func:
        return None
    
    return cost_func(current_level)

def calculate_inventory_value(inventory: Dict) -> int:
    """Calculate total value of all fish in inventory"""
    total_value = 0
    
    for rarity, fish_dict in inventory.get('Common', {}).items() if 'Common' in inventory else []:
        base_value = FISH_BASE_VALUES.get(rarity, 0)
        
        for fish_type, count in fish_dict.items():
            multiplier = FISH_MULTIPLIERS.get(fish_type, 1.0)
            fish_value = int(base_value * multiplier)
            total_value += fish_value * count
    
    return total_value

def sell_fish(user_data: Dict, rarity: str = None, fish_type: str = None, amount: int = None) -> Tuple[int, int]:
    """
    Sell fish from inventory
    Returns (total_value, fish_count)
    """
    inventory = user_data['inventory']
    total_value = 0
    fish_count = 0
    
    if rarity and fish_type:
        # Sell specific fish type
        if rarity in inventory and fish_type in inventory[rarity]:
            available = inventory[rarity][fish_type]
            to_sell = min(amount or available, available)
            
            if to_sell > 0:
                base_value = FISH_BASE_VALUES.get(rarity, 0)
                multiplier = FISH_MULTIPLIERS.get(fish_type, 1.0)
                fish_value = int(base_value * multiplier)
                
                total_value = fish_value * to_sell
                fish_count = to_sell
                
                inventory[rarity][fish_type] -= to_sell
                if inventory[rarity][fish_type] == 0:
                    del inventory[rarity][fish_type]
    
    elif rarity:
        # Sell all of a rarity
        if rarity in inventory:
            for fish_type, count in list(inventory[rarity].items()):
                base_value = FISH_BASE_VALUES.get(rarity, 0)
                multiplier = FISH_MULTIPLIERS.get(fish_type, 1.0)
                fish_value = int(base_value * multiplier)
                
                total_value += fish_value * count
                fish_count += count
            
            inventory[rarity] = {}
    
    else:
        # Sell all fish
        for rarity_tier in list(inventory.keys()):
            if rarity_tier == 'woodcutting':
                continue
            for fish_type, count in list(inventory[rarity_tier].items()):
                base_value = FISH_BASE_VALUES.get(rarity_tier, 0)
                multiplier = FISH_MULTIPLIERS.get(fish_type, 1.0)
                fish_value = int(base_value * multiplier)
                
                total_value += fish_value * count
                fish_count += count
            
            inventory[rarity_tier] = {}
    
    user_data['currency'] += total_value
    return total_value, fish_count

def sell_logs(user_data: Dict, rarity: str = None, log_type: str = None, amount: int = None) -> Tuple[int, int]:
    """
    Sell logs from inventory
    Returns (total_value, log_count)
    """
    inventory = user_data['inventory'].get('woodcutting', {})
    total_value = 0
    log_count = 0
    
    if rarity and log_type:
        # Sell specific log type
        if rarity in inventory and log_type in inventory[rarity]:
            available = inventory[rarity][log_type]
            to_sell = min(amount or available, available)
            
            if to_sell > 0:
                base_value = LOG_BASE_VALUES.get(rarity, 0)
                multiplier = LOG_MULTIPLIERS.get(log_type, 1.0)
                log_value = int(base_value * multiplier)
                
                total_value = log_value * to_sell
                log_count = to_sell
                
                inventory[rarity][log_type] -= to_sell
                if inventory[rarity][log_type] == 0:
                    del inventory[rarity][log_type]
    
    elif rarity:
        # Sell all of a rarity
        if rarity in inventory:
            for log_type, count in list(inventory[rarity].items()):
                base_value = LOG_BASE_VALUES.get(rarity, 0)
                multiplier = LOG_MULTIPLIERS.get(log_type, 1.0)
                log_value = int(base_value * multiplier)
                
                total_value += log_value * count
                log_count += count
            
            inventory[rarity] = {}
    
    else:
        # Sell all logs
        for rarity_tier in list(inventory.keys()):
            for log_type, count in list(inventory[rarity_tier].items()):
                base_value = LOG_BASE_VALUES.get(rarity_tier, 0)
                multiplier = LOG_MULTIPLIERS.get(log_type, 1.0)
                log_value = int(base_value * multiplier)
                
                total_value += log_value * count
                log_count += count
            
            inventory[rarity_tier] = {}
    
    user_data['currency'] += total_value
    return total_value, log_count

def get_shop_items() -> Dict:
    """Get available shop items with prices"""
    return {
        'hookSharpness': {
            'name': 'Hook Sharpness',
            'description': 'Increases chances of catching Rare+ fish',
            'max_level': UPGRADE_MAX_LEVEL
        },
        'lineStrength': {
            'name': 'Line Strength',
            'description': 'Increases chances of catching Epic+ fish',
            'max_level': UPGRADE_MAX_LEVEL
        },
        'bladeSharpness': {
            'name': 'Blade Sharpness',
            'description': 'Increases chances of harvesting Rare+ logs',
            'max_level': UPGRADE_MAX_LEVEL
        },
        'handleStrength': {
            'name': 'Handle Strength',
            'description': 'Increases chances of harvesting Epic+ logs',
            'max_level': UPGRADE_MAX_LEVEL
        }
    }
