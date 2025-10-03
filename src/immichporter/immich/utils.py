"""Immich specific utilities."""

import json
import os
from typing import Dict, Any
from pathlib import Path


def load_config(config_path: str = "immich_config.json") -> Dict[str, Any]:
    """Load Immich configuration from JSON file."""
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def save_config(
    config: Dict[str, Any], config_path: str = "immich_config.json"
) -> None:
    """Save Immich configuration to JSON file."""
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


def format_album_name(album_title: str) -> str:
    """Format album name for Immich."""
    # Remove special characters and normalize
    return album_title.strip()


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate Immich configuration."""
    required_fields = ["api_key", "server_url"]
    return all(field in config for field in required_fields)


def get_default_config_path() -> str:
    """Get default configuration file path."""
    return os.path.join(Path.home(), ".immichporter_config.json")
