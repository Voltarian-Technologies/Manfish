"""
Leaderboard generation and ranking
"""

from typing import Dict, List, Tuple
from .persistence import load_all_users
from .economy import get_rod_tier_index

async def get_richest_leaderboard(limit: int = 10) -> List[Tuple[str, int, int]]:
    """
    Get top users by currency
    Returns list of (username, user_id, currency)
    """
    users = await load_all_users()
    
    sorted_users = sorted(
        users.items(),
        key=lambda x: x[1].get('currency', 0),
        reverse=True
    )
    
    leaderboard = []
    for user_id, data in sorted_users[:limit]:
        username = data.get('username', f'User{user_id}')
        currency = data.get('currency', 0)
        leaderboard.append((username, user_id, currency))
    
    return leaderboard

async def get_catches_leaderboard(limit: int = 10) -> List[Tuple[str, int, int]]:
    """
    Get top users by total catches
    Returns list of (username, user_id, total_catches)
    """
    users = await load_all_users()
    
    sorted_users = sorted(
        users.items(),
        key=lambda x: x[1].get('stats', {}).get('totalCatches', 0),
        reverse=True
    )
    
    leaderboard = []
    for user_id, data in sorted_users[:limit]:
        username = data.get('username', f'User{user_id}')
        catches = data.get('stats', {}).get('totalCatches', 0)
        leaderboard.append((username, user_id, catches))
    
    return leaderboard

async def get_rod_leaderboard(limit: int = 10) -> List[Tuple[str, int, str, int]]:
    """
    Get top users by rod tier
    Returns list of (username, user_id, rod_tier, tier_index)
    """
    users = await load_all_users()
    
    sorted_users = sorted(
        users.items(),
        key=lambda x: get_rod_tier_index(x[1].get('rod', {}).get('tier', 'Starter Rod')),
        reverse=True
    )
    
    leaderboard = []
    for user_id, data in sorted_users[:limit]:
        username = data.get('username', f'User{user_id}')
        rod_tier = data.get('rod', {}).get('tier', 'Starter Rod')
        tier_index = get_rod_tier_index(rod_tier)
        leaderboard.append((username, user_id, rod_tier, tier_index))
    
    return leaderboard
