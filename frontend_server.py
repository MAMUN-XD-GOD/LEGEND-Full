from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import os
app = FastAPI()
BASE = os.path.join(os.path.dirname(__file__), '..', 'frontend')

@app.get('/')
async def index():
    return FileResponse(os.path.join(BASE,'index.html'))

@app.get('/signals.log')
async def signals():
    p = os.path.join(os.getcwd(), 'signals.log')
    if os.path.exists(p):
        return FileResponse(p)
    return JSONResponse({'signals':[]}, status_code=204)
