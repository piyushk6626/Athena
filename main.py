import json
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import functioncalling
import router

app = FastAPI()

@app.post("/")
async def receive_data_async(request: Request):
    # Get request body
    data_bytes = await request.body()
    data = data_bytes.decode('utf-8')

    # Create a structured message
    message = {
        "role": "user",
        "content": data
    }

    print(f"Received: {data}")

    # Process the query
    result = process_user_query(message)

    return JSONResponse(content=result, status_code=200)

def process_user_query(query):
    completion = functioncalling.AGI(messages=query)
    tool_call = completion.choices[0].message.tool_calls

    if tool_call:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        result = router.callfunction(name, args)
    else:
        result = {
            "type": "string",
            "data": completion.choices[0].message.content
        }
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
