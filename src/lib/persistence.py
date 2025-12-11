"""
Data persistence - User data loading and saving
"""

import json
import os
from typing import Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users')

def ensure_data_dir():
    """Ensure the data directory exists"""
    os.makedirs(DATA_DIR, exist_ok=True)

def get_user_file_path(user_id: int) -> str:
    """Get the file path for a user's data"""
    return os.path.join(DATA_DIR, f"{user_id}.json")

async def load_user_data(user_id: int, username: str = None) -> Dict[str, Any]:
    """Load user data, creating default if doesn't exist"""
    ensure_data_dir()
    file_path = get_user_file_path(user_id)
    
    if not os.path.exists(file_path):
        # Create default user data
        user_data = {
            'user_id': user_id,
            'username': username or f"User{user_id}",
            'currency': 0,
            'rod': {
                'tier': 'Starter Rod',
                'level': 1
            },
            'axe': {
                'tier': 'Starter Axe'
            },
            'upgrades': {
                'hookSharpness': 0,
                'lineStrength': 0,
                'bladeSharpness': 0,
                'handleStrength': 0
            },
            'inventory': {
                'Common': {},
                'Uncommon': {},
                'Rare': {},
                'Epic': {},
                'Legendary': {},
                'Mythic': {},
                'woodcutting': {}
            },
            'stats': {
                'totalCatches': 0,
                'totalChops': 0,
                'lastFishTimestamp': 0,
                'lastChopTimestamp': 0
            }
        }
        await save_user_data(user_id, user_data)
        return user_data
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure all required fields exist
            data.setdefault('user_id', user_id)
            data.setdefault('username', username or f"User{user_id}")
            data.setdefault('currency', 0)
            data.setdefault('rod', {'tier': 'Starter Rod', 'level': 1})
            data.setdefault('axe', {'tier': 'Starter Axe'})
            data.setdefault('upgrades', {})
            data.setdefault('inventory', {
                'Common': {}, 'Uncommon': {}, 'Rare': {}, 'Epic': {},
                'Legendary': {}, 'Mythic': {}, 'woodcutting': {}
            })
            data.setdefault('stats', {
                'totalCatches': 0, 'totalChops': 0,
                'lastFishTimestamp': 0, 'lastChopTimestamp': 0
            })
            
            # Update username if provided
            if username and username != data['username']:
                data['username'] = username
                await save_user_data(user_id, data)
                
            return data
    except Exception as e:
        print(f"Error loading user data for {user_id}: {e}")
        # Return default data
        return await load_user_data(user_id, username)

async def save_user_data(user_id: int, user_data: Dict[str, Any]) -> bool:
    """Save user data to file"""
    try:
        ensure_data_dir()
        file_path = get_user_file_path(user_id)
        
        # Make a clean copy without any non-serializable objects
        clean_data = {}
        for key, value in user_data.items():
            if isinstance(value, dict):
                clean_data[key] = {k: v for k, v in value.items()}
            else:
                clean_data[key] = value
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving user data for {user_id}: {e}")
        return False

async def load_all_users() -> Dict[int, Dict[str, Any]]:
    """Load all user data files"""
    ensure_data_dir()
    users = {}
    
    if not os.path.exists(DATA_DIR):
        return users
    
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            try:
                user_id = int(filename[:-5])  # Remove .json
                file_path = os.path.join(DATA_DIR, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    users[user_id] = user_data
            except (ValueError, json.JSONDecodeError) as e:
                print(f"Error loading {filename}: {e}")
                continue
    
    return users
