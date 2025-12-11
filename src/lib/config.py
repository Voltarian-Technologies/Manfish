import json
import os

# Define paths to configuration files
CONFIG_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'config')
SETTINGS_FILE = os.path.join(CONFIG_DIR, 'settings.json')
RATES_FILE = os.path.join(CONFIG_DIR, 'rates.json')
EMOJI_FILE = os.path.join(CONFIG_DIR, 'emoji.json')
COSTS_FILE = os.path.join(CONFIG_DIR, 'costs.json')

# Global variables to store loaded configurations
_settings_config = {}
_rates_config = {}
_emoji_config = {}
_costs_config = {}

def _load_config_file(file_path):
    """Helper function to load a JSON configuration file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_all_configs():
    """Loads all configuration files into global variables."""
    global _settings_config, _rates_config, _emoji_config, _costs_config
    
    print("Loading configurations...")
    _settings_config = _load_config_file(SETTINGS_FILE)
    print(f"  Loaded {SETTINGS_FILE}")
    _rates_config = _load_config_file(RATES_FILE)
    print(f"  Loaded {RATES_FILE}")
    _emoji_config = _load_config_file(EMOJI_FILE)
    print(f"  Loaded {EMOJI_FILE}")
    _costs_config = _load_config_file(COSTS_FILE)
    print(f"  Loaded {COSTS_FILE}")
    print("All configurations loaded.")

# --- Getters ---
def get_settings_config():
    """Returns the loaded settings configuration."""
    return _settings_config

def get_rates_config():
    """Returns the loaded rates configuration."""
    return _rates_config

def get_emoji_config():
    """Returns the loaded emoji configuration."""
    return _emoji_config

def get_costs_config():
    """Returns the loaded costs configuration."""
    return _costs_config

# --- Updaters ---
def update_settings_config(new_settings):
    """Updates the settings configuration and saves it to file."""
    global _settings_config
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_settings, f, indent=2)
        _settings_config = new_settings # Update in-memory config
        return True
    except Exception as e:
        print(f"Error saving settings config: {e}")
        return False

def update_emoji_config(new_emojis):
    """Updates the emoji configuration and saves it to file."""
    global _emoji_config
    try:
        with open(EMOJI_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_emojis, f, indent=2)
        _emoji_config = new_emojis # Update in-memory config
        return True
    except Exception as e:
        print(f"Error saving emoji config: {e}")
        return False

def update_rates_config(new_rates):
    """Updates the rates configuration and saves it to file."""
    global _rates_config
    try:
        with open(RATES_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_rates, f, indent=2)
        _rates_config = new_rates # Update in-memory config
        return True
    except Exception as e:
        print(f"Error saving rates config: {e}")
        return False

# --- Specific Setting Getters ---

def get_fish_cooldown():
    """Returns the fishing cooldown in seconds."""
    return _settings_config.get('fishCooldown', 60) # Default to 60 seconds

def get_wood_cooldown():
    """Returns the woodcutting cooldown in seconds."""
    return _settings_config.get('chopCooldown', 60) # Default to 60 seconds

def get_golden_bite_chance():
    """Returns the golden bite chance as a percentage (e.g., 1.0 for 1%)."""
    return _settings_config.get('goldenBiteChance', 1.0) # Default to 1%

def get_timber_bite_chance():
    """Returns the timber bite chance as a percentage (e.g., 1.0 for 1%)."""
    return _settings_config.get('timberBiteChance', 1.0) # Default to 1%


# Initial load when the module is imported.
# This ensures configs are available immediately.
# The load_all_configs() call in bot.py will re-load them on startup
# and print the status messages.
try:
    load_all_configs()
except FileNotFoundError as e:
    print(f"Initial config load failed: {e}. Will retry on bot ready.")
except Exception as e:
    print(f"An unexpected error occurred during initial config load: {e}")