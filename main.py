from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from limiter import is_allowed

app = FastAPI()

@app.get("/check")
async def check_rate(request: Request):
    client_ip = request.client.host
    response = is_allowed(client_ip)

    if response:
        return JSONResponse(content={"message": "allowed"}, status_code=200)
    else:
        return JSONResponse(content={"message": "too many requests"}, status_code=429)
        

