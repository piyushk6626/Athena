"""
Function Calling Module for Athena Virtual Assistant

This module handles communication with OpenAI's API for function calling capabilities.
It loads tools from a JSON file and provides functionality to interact with language models.
"""

import json
import os
import logging
from typing import List, Dict, Any, Optional

from openai import OpenAI

# Import centralized configuration
import config

# Configure logging
logger = logging.getLogger(__name__)


def load_tools_from_json(filename: str = config.APP_SETTINGS["TOOLS_FILE"]) -> List[Dict[str, Any]]:
    """
    Load tool definitions from a JSON file.
    
    Args:
        filename: Path to the JSON file containing tool definitions
        
    Returns:
        List of tool definitions, each containing type and function specifications
        
    Raises:
        FileNotFoundError: If the tools file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if not os.path.exists(filename):
        logger.warning(f"Tools file {filename} not found")
        return []

    try:
        with open(filename, 'r') as f:
            tools = json.load(f)
        logger.info(f"Successfully loaded {len(tools)} tools from {filename}")
        return tools
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing tools file {filename}: {e}")
        raise


# Load tool definitions
TOOLS = load_tools_from_json()
logger.info(f"Loaded {len(TOOLS)} tools")

# Initialize OpenAI client
client = OpenAI(api_key=config.API_KEYS["OPENAI_API_KEY"])


def AGI(messages: List[Dict[str, str]], model: str = config.APP_SETTINGS["DEFAULT_LLM_MODEL"]) -> Any:
    """
    Send messages to the language model and get completions with potential tool calls.
    
    Args:
        messages: List of message objects with role and content keys
        model: The OpenAI model to use (defaults to value from config)
        
    Returns:
        OpenAI completion object containing the model's response and any tool calls
        
    Raises:
        Exception: If there's an error communicating with the OpenAI API
    """
    try:
        logger.info(f"Sending request to {model} with {len(messages)} messages")
        completion = client.chat.completions.create(
            model=model,
            messages=messages,        
            tools=TOOLS,
            tool_choice="auto"
        )
        return completion
    except Exception as e:
        logger.error(f"Error in OpenAI API call: {e}")
        raise
