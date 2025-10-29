from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import time
import RobotController

Motor = RobotController.MotorDriver()

app = FastAPI(
    title="Robot API",
    description="An API to perform robot actions of forward, backward, left, right turns.",
    version="1.0.0",
)

favicon_path = "favicon.ico" 

@app.get("/favicon.ico")
async def get_favicon():
    try:
        return FileResponse(favicon_path)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Favicon not found")

@app.post("/move/forward", status_code=200)
async def move_forward(speed, ttime):
    ttime = int(ttime)
    speed = int(speed)
    Motor.MotorRun(0, 'forward', speed)
    Motor.MotorRun(1, 'backward', speed)
    time.sleep(ttime)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    return {"status": "success"}
    
@app.post("/move/right", status_code=200)    
async def move_right(speed, ttime):
    ttime = int(ttime)
    speed = int(speed)
    Motor.MotorRun(0, 'forward', speed)
    time.sleep(ttime)
    Motor.MotorStop(0)
    return {"status": "success"}

@app.post("/move/left", status_code=200)    
async def move_left(speed, ttime):
    ttime = int(ttime)
    speed = int(speed)
    Motor.MotorRun(1, 'forward', speed)
    time.sleep(ttime)
    Motor.MotorStop(1)
    return {"status": "success"}

@app.post("/move/backward", status_code=200)
async def move_backward(speed, ttime):
    ttime = int(ttime)
    speed = int(speed)
    Motor.MotorRun(0, 'backward', speed)
    Motor.MotorRun(1, 'forward', speed)
    time.sleep(ttime)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    return {"status": "success"}

@app.post("/stop", status_code=200)
async def stop():
    Motor.MotorStop()
    return {"status": "success"}
