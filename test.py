

import json
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import functioncalling
import router



def process_user_query(query):
    message = [{
        "role": "user",
        "content": query    
    }]

    
    completion = functioncalling.AGI(messages=message)
    tool_call = completion.choices[0].message.tool_calls
    print(tool_call)
    if tool_call:  
        for tool_call in completion.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            result = router.callfunction(name, args)
    else:
        result = {
            "type": "string",
            "data": completion.choices[0].message.content
        }
    
    return result


result = process_user_query("i want to wantch a movie tommrow afternoon in pune")
print(result)