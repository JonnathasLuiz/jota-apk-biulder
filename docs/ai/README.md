# AI Agent Documentation - Jota APK Builder

This document provides technical details for other AI agents interacting with or maintaining this system.

## System Architecture
- **Backend:** FastAPI (Python)
- **Task Queue:** Celery with Redis broker/backend
- **Build Engine:** Subprocess calls to `gradlew` (Native) or `buildozer` (Python/Kivy)
- **Storage:** Local file system under `storage/apks/`

## API Specification

### POST `/api/v1/build`
- **Purpose:** Initiates a background build task.
- **Payload Schema:** `{"repo_url": str}` (must be a valid URL).
- **Logic:** Validates URL, triggers `app.tasks.build_apk_task` asynchronously, returns Celery task UUID.

### GET `/api/v1/status/{task_id}`
- **Purpose:** Polls task status and retrieves logs/results.
- **Returns:**
    - `task_id`: UUID
    - `status`: Celery state (PENDING, PROCESSING, SUCCESS, FAILURE, etc.)
    - `logs`: Combined stdout/stderr from the build process or custom error messages.
    - `download_url`: Present only if `status == "SUCCESS"`.

### GET `/api/v1/download/{task_id}`
- **Purpose:** Streams the generated APK file.
- **Media Type:** `application/vnd.android.package-archive`

## Task Lifecycle (`app/tasks.py`)
1. **Setup:** Create `tempfile.TemporaryDirectory`.
2. **Clone:** `git clone` using `GitPython`.
3. **Detection:** Checks for presence of `build.gradle` (Native) or `buildozer.spec` (Python).
4. **Execution:**
   - Native: `chmod +x gradlew` -> `./gradlew assembleDebug`
   - Python: `buildozer android debug`
5. **Artifact Collection:** Locates `.apk` in standard output paths (`app/build/outputs/apk/debug` or `bin/`).
6. **Cleanup:** Moves APK to permanent storage, temporary directory is auto-deleted.

## Error Handling
The system captures `stdout` and `stderr` using `subprocess.run(capture_output=True)`. These logs are returned in the status endpoint when a build fails to aid debugging.

## Maintenance Notes
- Ensure `redis-server` is running.
- Ensure Android SDK, NDK, and Buildozer are correctly configured in the host environment PATH.
- `storage/apks/` must be writable by the worker process.
