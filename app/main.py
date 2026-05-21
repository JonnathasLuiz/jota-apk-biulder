import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
from pathlib import Path
from .worker import celery_app
from .tasks import build_apk_task

app = FastAPI(title="Jota APK Builder API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STORAGE_DIR = Path("storage/apks")

class BuildRequest(BaseModel):
    repo_url: HttpUrl

class BuildResponse(BaseModel):
    task_id: str
    status: str

class StatusResponse(BaseModel):
    task_id: str
    status: str
    logs: str = ""
    download_url: str = None

@app.post("/api/v1/build", response_model=BuildResponse, status_code=202)
async def build_apk(request: BuildRequest):
    # Simple sanitization is handled by HttpUrl pydantic type
    task = build_apk_task.delay(str(request.repo_url))
    return {"task_id": task.id, "status": "PENDING"}

@app.get("/api/v1/status/{task_id}", response_model=StatusResponse)
async def get_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)

    status = task_result.status
    result = task_result.result if task_result.ready() else None

    # Check if task is still processing but has meta updates
    logs = ""
    if isinstance(task_result.info, dict):
        logs = task_result.info.get("logs", "")
        if task_result.status == "PROCESSING":
             # Celery standard is STARTED, but I used PROCESSING in update_state
             pass

    response_data = {
        "task_id": task_id,
        "status": status,
        "logs": logs
    }

    if result and isinstance(result, dict):
        response_data["status"] = result.get("status", status)
        response_data["logs"] = result.get("logs", logs)
        if result.get("download_url"):
            response_data["download_url"] = result.get("download_url")

    return response_data

@app.get("/api/v1/download/{task_id}")
async def download_apk(task_id: str):
    apk_path = STORAGE_DIR / f"{task_id}.apk"
    if not apk_path.exists():
        raise HTTPException(status_code=404, detail="APK not found or build still in progress.")

    return FileResponse(
        path=apk_path,
        filename=f"{task_id}.apk",
        media_type="application/vnd.android.package-archive"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
