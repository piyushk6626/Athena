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
    history = data.get("history", [])
    # Create a structured message

    print(f"Received: {data}")

    # Process the query
    result = process_user_query(history)
    # result = {
    #     "type": "string",
    #     "data": "Hello, World!"
    # }


    # jsresult = json.dumps(result)

    # print(jsresult)


    return JSONResponse(content=result, status_code=200)

def process_user_query(query):
    # message = [{
    #     "role": "user",
    #     "content": query    
    # }]

    
    completion = functioncalling.AGI(query)
    tool_call = completion.choices[0].message.tool_calls
    print(tool_call)
    if tool_call:  
        for tool_call in completion.choices[0].message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            result = router.callfunction(name, args)
    else:
        result = {
            "type": "text",
            "data": completion.choices[0].message.content
        }
    
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
