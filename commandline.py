import json
import functioncalling
import router
import json

def safe_json_dumps(data):
    try:
        return json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    except ValueError as e:
        print("JSON Serialization Error:", e)
        return "{}"  # Return an empty JSON object to avoid crashes

def process_user_query(history):
    completion = functioncalling.AGI(history)
    tool_call = completion.choices[0].message.tool_calls
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

def main():
    history = []
    
    

    while True:
        query = input("You: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        history.append({"role": "user", "content": query})
        result = process_user_query(history)

        # Use safe_json_dumps when handling response data
        response = safe_json_dumps(result.get("data", "Error processing query."))

        print(f"Assistant: {response}")

        history.append({"role": "assistant", "content": response})
if __name__ == "__main__":
    main()
