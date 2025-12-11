"""
User data persistence layer using JSON files
Atomic writes with per-user locks to prevent corruption
"""

import json
import os
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

DATA_DIR = 'data'
_user_locks: Dict[str, asyncio.Lock] = {}

def ensure_data_dir():
    """Ensure the data directory exists"""
    os.makedirs(DATA_DIR, exist_ok=True)

def get_user_filepath(user_id: int) -> str:
    """Get the filepath for a user's data file"""
    return os.path.join(DATA_DIR, f"{user_id}.json")

def get_user_lock(user_id: int) -> asyncio.Lock:
    """Get or create a lock for a specific user"""
    if user_id not in _user_locks:
        _user_locks[user_id] = asyncio.Lock()
    return _user_locks[user_id]

def create_default_user_data(user_id: int, username: str) -> Dict[str, Any]:
    """Create default user data structure"""
    return {
        'id': str(user_id),
        'username': username,
        'currency': 0,
        'rod': {
            'tier': 'Starter Rod',
            'level': 1
        },
        'axe': {
            'tier': 'Starter Axe',
            'level': 1
        },
        'upgrades': {
            'hookSharpness': 0,
            'lineStrength': 0,
            'bladeSharpness': 0,
            'handleStrength': 0
        },
        'stats': {
            'totalCatches': 0,
            'lastFishTimestamp': 0,
            'totalChops': 0,
            'lastChopTimestamp': 0
        },
        'inventory': {
            'Common': {},
            'Uncommon': {},
            'Rare': {},
            'Epic': {},
            'Legendary': {},
            'Mythic': {},
            'woodcutting': {
                'Common': {},
                'Uncommon': {},
                'Rare': {},
                'Epic': {},
                'Legendary': {},
                'Mythic': {}
            }
        }
    }

async def load_user_data(user_id: int, username: str) -> Dict[str, Any]:
    """
    Load user data from JSON file
    Creates default data if file doesn't exist
    """
    ensure_data_dir()
    lock = get_user_lock(user_id)
    
    async with lock:
        filepath = get_user_filepath(user_id)
        
        if not os.path.exists(filepath):
            # Create new user data
            user_data = create_default_user_data(user_id, username)
            await save_user_data(user_id, user_data, skip_lock=True)
            return user_data
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
                # Update username if changed
                user_data['username'] = username
                return user_data
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Error loading user {user_id} data: {e}")
            print(f"Creating backup and resetting user data...")
            
            # Backup corrupted file
            backup_file = f"{filepath}.backup.{int(datetime.now().timestamp())}"
            try:
                os.rename(filepath, backup_file)
            except:
                pass
            
            # Return default data
            user_data = create_default_user_data(user_id, username)
            await save_user_data(user_id, user_data, skip_lock=True)
            return user_data

async def save_user_data(user_id: int, data: Dict[str, Any], skip_lock: bool = False):
    """
    Save user data to JSON file atomically
    Uses temp file + rename to prevent corruption
    """
    ensure_data_dir()
    
    async def _save():
        filepath = get_user_filepath(user_id)
        temp_filepath = filepath + '.tmp'
        
        try:
            # Write to temp file
            with open(temp_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            # Atomic rename
            os.replace(temp_filepath, filepath)
        except Exception as e:
            print(f"❌ Error saving user {user_id} data: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_filepath):
                try:
                    os.remove(temp_filepath)
                except:
                    pass
    
    if skip_lock:
        await _save()
    else:
        lock = get_user_lock(user_id)
        async with lock:
            await _save()

async def get_all_user_files() -> list:
    """Get all user data files"""
    ensure_data_dir()
    files = []
    
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json') and not filename.endswith('.tmp'):
            filepath = os.path.join(DATA_DIR, filename)
            files.append(filepath)
    
    return files

async def load_all_users() -> Dict[int, Dict[str, Any]]:
    """Load all user data (for leaderboards)"""
    users = {}
    files = await get_all_user_files()
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                user_id = int(data['id'])
                users[user_id] = data
        except Exception as e:
            print(f"⚠️ Error loading {filepath}: {e}")
            continue
    
    return users
