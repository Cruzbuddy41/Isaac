from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import RobotController

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
async def move_forward():
    RobotController.forward()
    return {"status": "success"}

@app.post("/stop", status_code=200)
async def stop():
    RobotController.stop()
    return {"status": "success"}
