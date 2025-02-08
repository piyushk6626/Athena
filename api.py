from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import time 
app = FastAPI()

# Define the POST endpoint with correct async handling
@app.post("/")
async def receive_data_async(request: Request):
    # Get request body (await the coroutine)
    data_bytes = await request.body()
    data = data_bytes.decode('utf-8')
    time.sleep(3)
    #instead of this direct return first process it then return 
    print(f"Received: {data}")
    
    return PlainTextResponse(
        content=f"Received your async message: {data}",
        status_code=200
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)