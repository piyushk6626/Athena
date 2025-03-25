"""
Configuration Module for Athena Virtual Assistant

This module centralizes configuration settings for the Athena virtual assistant,
including API keys, service endpoints, and application settings.
"""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv(override=True)

# API keys and credentials
API_KEYS = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "SPOTIFY_CLIENT_ID": os.getenv("SPOTIFY_CLIENT_ID"),
    "SPOTIFY_CLIENT_SECRET": os.getenv("SPOTIFY_CLIENT_SECRET"),
    "EMAIL_ACCOUNT": os.getenv("EMAIL_ACCOUNT"),
    "EMAIL_PASSWORD": os.getenv("EMAIL_PASSWORD"),
}

# Application settings
APP_SETTINGS = {
    "DEBUG": True,
    "HOST": "127.0.0.1",
    "PORT": 3000,
    "TOOLS_FILE": "tools.json",
    "DEFAULT_LLM_MODEL": "gpt-4o",
}

# Validate critical configuration
def validate_config() -> None:
    """
    Validate that critical configuration settings are present.
    
    Raises:
        EnvironmentError: If any required configuration is missing
    """
    missing_keys = []
    
    # Check for required API keys
    if not API_KEYS["OPENAI_API_KEY"]:
        missing_keys.append("OPENAI_API_KEY")
    
    # Raise error if any required keys are missing
    if missing_keys:
        error_msg = f"Missing required environment variables: {', '.join(missing_keys)}"
        logger.error(error_msg)
        raise EnvironmentError(error_msg)

# Validate configuration on module import
validate_config() 