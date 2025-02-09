import json
import functioncalling
import router

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

        response = result.get("data", "Error processing query.")
        print(f"Assistant: {response}")

        history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
