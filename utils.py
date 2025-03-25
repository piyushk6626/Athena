"""
Utility Module for Athena Virtual Assistant

This module provides utility functions used across the Athena virtual assistant
application, including data processing, validation, and common operations.
"""

import json
import logging
from typing import Dict, Any, List, Union, Optional

# Configure logging
logger = logging.getLogger(__name__)


def clean_json(input_json: Union[Dict, str]) -> Dict:
    """
    Clean and normalize JSON data from various input formats.
    
    Args:
        input_json: Either a dictionary or a JSON string to be cleaned
        
    Returns:
        Dict: Normalized dictionary with properly parsed fields
    """
    # If input_json is already a dictionary, use it directly
    if isinstance(input_json, dict):
        data_dict = input_json
    else:
        data_dict = json.loads(input_json)

    # Ensure the 'data' field is properly parsed as a list
    if isinstance(data_dict.get("data"), str):
        try:
            data_dict["data"] = json.loads(data_dict["data"])  # Convert string to list
        except json.JSONDecodeError:
            logger.warning("Failed to parse 'data' field as JSON")
            # If it fails, keep it as is

    return data_dict


def format_error_response(message: str, details: Optional[Any] = None) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        message: The main error message
        details: Optional details about the error (exception info, etc.)
        
    Returns:
        Dict: A standardized error response dictionary
    """
    response = {
        "type": "error",
        "data": {
            "message": message
        }
    }
    
    if details:
        response["data"]["details"] = details
        
    return response


def format_success_response(data: Any, message: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: The main response data
        message: Optional success message
        
    Returns:
        Dict: A standardized success response dictionary
    """
    response = {
        "type": "success",
        "data": data
    }
    
    if message:
        response["message"] = message
        
    return response


def format_text_response(text: str) -> Dict[str, Any]:
    """
    Create a standardized text response.
    
    Args:
        text: The text content to include in the response
        
    Returns:
        Dict: A standardized text response dictionary
    """
    return {
        "type": "text",
        "data": text
    }


def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """
    Validate that all required fields are present in a dictionary.
    
    Args:
        data: The dictionary to validate
        required_fields: List of field names that should be present
        
    Returns:
        List: Empty list if all fields are present, otherwise list of missing fields
    """
    missing_fields = []
    
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
    
    return missing_fields 