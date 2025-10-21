from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import RobotController
import uuid
from fastapi.responses import FileResponse

app = FastAPI(
    title="Robot API",
    description="An API to perform robot actions of forward, backward, left, right turns.",
    version="1.0.0",
)

favicon_path = "path/to/your/favicon.ico"

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse(favicon_path)

@app.post("/move/forward", status_code=200)
async def move_forward(steps: int):
    RobotController.forward(15)
    return {"status": "success"}

@app.post("/stop", status_code=200)
async def stop():
    RobotController.stop()
    return {"status": "success"}
