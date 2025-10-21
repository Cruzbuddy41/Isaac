from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import RobotController
import uuid

app = FastAPI(
    title="Robot API",
    description="An API to perform robot actions of forward, backward, left, right turns.",
    version="1.0.0",
)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Robot API"}
    
@app.post("/move/forward", status_code=200)
async def move_forward(steps: int):
    RobotController.forward(15)
    return {"status": "success"}

@app.post("/stop", status_code=200)
async def stop():
    RobotController.stop()
    return {"status": "success"}
