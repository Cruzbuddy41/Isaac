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
async def move_forward(speed):
    print(type(speed))
    speed = 50
    Motor.MotorRun(0, 'forward', speed)
    Motor.MotorRun(1, 'forward', speed)
    time.sleep(2)
    Motor.MotorStop(0)
    Motor.MotorStop(1)
    return {"status": "success"}

@app.post("/stop", status_code=200)
async def stop():
    Motor.MotorStop()
    return {"status": "success"}
