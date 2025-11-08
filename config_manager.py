"""
Configuration Manager
Handles loading and saving app configuration including NFC mappings
"""
import json
import os
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "music_library_path": "music",
    "stop_nfc_id": None,
    "volume": 0.7,
    "nfc_mappings": {},
    "debug_mode": False
}


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_file="config.json"):
        """
        Initialize config manager
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = DEFAULT_CONFIG.copy()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                logger.info("Using default configuration")
        else:
            logger.info("No config file found, using defaults")
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
    
    def set_stop_nfc_id(self, nfc_id):
        """Set the NFC ID that stops music playback"""
        self.config["stop_nfc_id"] = nfc_id
        logger.info(f"Stop NFC ID set to: {nfc_id}")
    
    def is_stop_nfc(self, nfc_id):
        """Check if NFC ID is the stop command"""
        return nfc_id == self.config.get("stop_nfc_id")
    
    def get_music_library_path(self):
        """Get music library path"""
        return self.config.get("music_library_path", "music")
    
    def set_music_library_path(self, path):
        """Set music library path"""
        self.config["music_library_path"] = path

