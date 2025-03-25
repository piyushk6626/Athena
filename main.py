"""
Athena Virtual Assistant FastAPI Server

This module provides the main FastAPI server for the Athena virtual assistant.
It handles user queries, processes them through a language model, and routes
function calls to appropriate handlers.
"""

import json
import logging
from typing import Dict, Any, List, Union

from fastapi import FastAPI, Request

import config
import functioncalling
import router
import utils

# Configure logging
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Athena Virtual Assistant API",
    description="API for processing user queries and interacting with various services",
    version="1.0.0",
    debug=config.APP_SETTINGS["DEBUG"]
)


@app.post("/")
async def receive_data_async(request: Request) -> Dict:
    """
    Process incoming HTTP requests with user queries.
    
    Args:
        request: FastAPI Request object containing the user query
        
    Returns:
        Dict: Response data containing either function call results or text response
    """
    try:
        # Extract request body
        data_bytes = await request.body()
        data = data_bytes.decode('utf-8')
        logger.info(f"Received request: {data[:100]}...")  # Log first 100 chars of request
        
        # Process the query and return result
        result = process_user_query(data)
        return result
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return utils.format_error_response(f"Error processing request: {str(e)}")


def process_user_query(query: str) -> Dict:
    """
    Process a user query by sending it to the language model and handling the response.
    
    The function sends the query to the language model, which may return:
    1. A tool call - in this case, the function routes the call to the appropriate handler
    2. A text response - in this case, the function returns the text directly
    
    Args:
        query: The user's input query
        
    Returns:
        Dict: Response containing either the result of a function call or text content
    """
    # Format message for the language model
    message = [{
        "role": "user",
        "content": query    
    }]

    logger.info(f"Sending message to language model: {message}")
    
    # Get completion from language model
    completion = functioncalling.AGI(message)
    tool_calls = completion.choices[0].message.tool_calls
    
    if tool_calls:  
        logger.info(f"Received tool calls: {tool_calls}")
        # Process tool calls
        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            logger.info(f"Executing function: {name} with args: {args}")
            
            # Route the function call to the appropriate handler
            result = router.callfunction(name, args)
            
            # If result is None, return an error
            if result is None:
                return utils.format_error_response(f"Function '{name}' not found or failed to execute")
    else:
        # If no tool call, return the text response directly
        logger.info("No tool calls received, returning text response")
        result = utils.format_text_response(completion.choices[0].message.content)
    
    return utils.clean_json(result)


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Athena Virtual Assistant API server")
    uvicorn.run(
        app, 
        host=config.APP_SETTINGS["HOST"], 
        port=config.APP_SETTINGS["PORT"]
    )
