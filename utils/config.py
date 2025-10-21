import yaml
import os
from typing import Dict, List, Any, Optional

CONFIG_FILE = 'config.yaml'

class ConfigManager:
    """Manages application configuration including channel management."""

    def __init__(self, config_path: str = CONFIG_FILE):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Configuration file '{self.config_path}' not found. "
                f"Please create one based on config.example.yaml"
            )

        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Validate required sections
        required_sections = ['youtube', 'openai', 'database', 'channels']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required configuration section: '{section}'")

        return config

    def save_config(self) -> None:
        """Save current configuration to YAML file."""
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)

    # YouTube settings
    def get_youtube_settings(self) -> Dict[str, Any]:
        """Get YouTube API settings."""
        return self.config.get('youtube', {})

    def get_max_results(self) -> int:
        """Get maximum results per channel."""
        return self.config.get('youtube', {}).get('max_results', 20)

    # OpenAI settings
    def get_openai_settings(self) -> Dict[str, Any]:
        """Get OpenAI API settings."""
        return self.config.get('openai', {})

    def get_model(self) -> str:
        """Get OpenAI model name."""
        return self.config.get('openai', {}).get('model', 'gpt-3.5-turbo-16k')

    def get_temperature(self) -> float:
        """Get OpenAI temperature setting."""
        return self.config.get('openai', {}).get('temperature', 0)

    def get_system_prompt(self) -> str:
        """Get system prompt for AI analysis."""
        return self.config.get('openai', {}).get(
            'system_prompt',
            "You are an AI capable of summarizing YouTube video content based on its transcript."
        )

    def get_user_prompt_template(self) -> str:
        """Get user prompt template."""
        return self.config.get('openai', {}).get(
            'user_prompt_template',
            "Generate a concise summary of the YouTube video using this transcript: {transcript}."
        )

    # Database settings
    def get_database_settings(self) -> Dict[str, Any]:
        """Get database connection settings."""
        return self.config.get('database', {})

    def get_db_server(self) -> str:
        """Get database server."""
        return self.config.get('database', {}).get('server', 'server')

    def get_db_name(self) -> str:
        """Get database name."""
        return self.config.get('database', {}).get('database', 'database')

    def get_db_driver(self) -> str:
        """Get database driver."""
        return self.config.get('database', {}).get('driver', '{ODBC Driver 17 for SQL Server}')

    # Channel management
    def get_channels(self, enabled_only: bool = True) -> List[Dict[str, Any]]:
        """
        Get list of channels.

        Args:
            enabled_only: If True, return only enabled channels

        Returns:
            List of channel dictionaries
        """
        channels = self.config.get('channels', [])
        if enabled_only:
            return [ch for ch in channels if ch.get('enabled', True)]
        return channels

    def get_channel_ids(self, enabled_only: bool = True) -> List[str]:
        """
        Get list of channel IDs.

        Args:
            enabled_only: If True, return only enabled channel IDs

        Returns:
            List of channel ID strings
        """
        channels = self.get_channels(enabled_only)
        return [ch['id'] for ch in channels if 'id' in ch]

    def add_channel(self, channel_id: str, name: str = None, enabled: bool = True) -> bool:
        """
        Add a new channel to the configuration.

        Args:
            channel_id: YouTube channel ID
            name: Optional channel name/description
            enabled: Whether the channel is enabled

        Returns:
            True if added successfully, False if channel already exists
        """
        # Check if channel already exists
        if any(ch.get('id') == channel_id for ch in self.config.get('channels', [])):
            return False

        new_channel = {
            'id': channel_id,
            'name': name or f"Channel {channel_id}",
            'enabled': enabled
        }

        if 'channels' not in self.config:
            self.config['channels'] = []

        self.config['channels'].append(new_channel)
        self.save_config()
        return True

    def remove_channel(self, channel_id: str) -> bool:
        """
        Remove a channel from the configuration.

        Args:
            channel_id: YouTube channel ID to remove

        Returns:
            True if removed successfully, False if channel not found
        """
        channels = self.config.get('channels', [])
        original_length = len(channels)

        self.config['channels'] = [ch for ch in channels if ch.get('id') != channel_id]

        if len(self.config['channels']) < original_length:
            self.save_config()
            return True
        return False

    def enable_channel(self, channel_id: str) -> bool:
        """Enable a channel."""
        return self._set_channel_status(channel_id, True)

    def disable_channel(self, channel_id: str) -> bool:
        """Disable a channel."""
        return self._set_channel_status(channel_id, False)

    def _set_channel_status(self, channel_id: str, enabled: bool) -> bool:
        """Set channel enabled status."""
        channels = self.config.get('channels', [])
        for channel in channels:
            if channel.get('id') == channel_id:
                channel['enabled'] = enabled
                self.save_config()
                return True
        return False

    def update_channel_name(self, channel_id: str, name: str) -> bool:
        """
        Update a channel's name.

        Args:
            channel_id: YouTube channel ID
            name: New name for the channel

        Returns:
            True if updated successfully, False if channel not found
        """
        channels = self.config.get('channels', [])
        for channel in channels:
            if channel.get('id') == channel_id:
                channel['name'] = name
                self.save_config()
                return True
        return False


# Global config instance
_config_instance: Optional[ConfigManager] = None

def get_config() -> ConfigManager:
    """Get or create the global configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
