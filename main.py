import json
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import functioncalling
import router

app = FastAPI()


def clean_json(input_json):
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
            pass  # If it fails, keep it as is

    return data_dict# Return cleaned dictionary

# def unformat_json(data) -> str:
#     """
#     Takes a JSON string or dictionary and returns a minified JSON string.
    
#     :param data: JSON string or dictionary
#     :return: Minified JSON string
#     """
#     try:
#         if isinstance(data, str):
#             parsed = json.loads(data)  # Convert string to dict
#         elif isinstance(data, dict):
#             parsed = data  # Already a dict, use it directly
#         else:
#             return "Invalid JSON input"
        
#         return json.dumps(parsed, separators=(",", ":"))  # Minify JSON
#     except json.JSONDecodeError:
#         return "Invalid JSON input"

@app.post("/")
async def receive_data_async(request: Request):
    # Get request body
    data_bytes = await request.body()
    data = data_bytes.decode('utf-8')
    #history = data.get("history", [])
    # Create a structured message

    print(f"Received: {data}")

    # Process the query
    result = process_user_query(data)
    # result = {
    #     "type": "string",
    #     "data": "Hello, World!"
    # }


    # jsresult = json.dumps(result)

    # print(jsresult)


    # return JSONResponse(content=result, status_code=200)
    return result

def process_user_query(query):
    message = [{
        "role": "user",
        "content": query    
    }]

    
    completion = functioncalling.AGI(message)
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
    
    return clean_json(result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
