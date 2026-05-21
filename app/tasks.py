import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from git import Repo
from .worker import celery_app

STORAGE_DIR = Path("storage/apks")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def _build_apk_logic(self, repo_url: str):
    # Determine task_id safely
    if self and hasattr(self, 'request') and self.request and self.request.id:
        task_id = self.request.id
    else:
        task_id = "test-task-id"

    def safe_update_state(state, meta):
        if self and hasattr(self, 'update_state'):
             try:
                 self.update_state(state=state, meta=meta)
             except Exception:
                 pass

    safe_update_state(state="PROCESSING", meta={"logs": "Starting build process..."})

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # 1. Clone
        try:
            safe_update_state(state="PROCESSING", meta={"logs": f"Cloning repository: {repo_url}"})
            Repo.clone_from(repo_url, tmp_path)
        except Exception as e:
            return {"status": "FAILED", "logs": f"Clone failed: {str(e)}"}

        # 2. Detect Stack
        stack = None
        if (tmp_path / "build.gradle").exists() or (tmp_path / "build.gradle.kts").exists() or (tmp_path / "app/build.gradle").exists() or (tmp_path / "app/build.gradle.kts").exists():
            stack = "native"
        elif (tmp_path / "buildozer.spec").exists():
            stack = "python"

        if not stack:
            return {"status": "FAILED", "logs": "No compatible build stack detected (Gradle or Buildozer)."}

        # 3. Build
        logs = ""
        try:
            if stack == "native":
                gradlew = tmp_path / "gradlew"
                if gradlew.exists():
                    try:
                        os.chmod(gradlew, 0o755)
                        cmd = ["./gradlew", "assembleDebug"]
                    except Exception:
                        # Might fail in some environments or during tests if gradlew isn't real
                        cmd = ["gradle", "assembleDebug"]
                else:
                    # Fallback if gradlew is missing but it's a gradle project
                    cmd = ["gradle", "assembleDebug"]

                safe_update_state(state="PROCESSING", meta={"logs": f"Running Gradle build..."})
                result = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True)
            else: # python/kivy
                safe_update_state(state="PROCESSING", meta={"logs": f"Running Buildozer..."})
                cmd = ["buildozer", "android", "debug"]
                result = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True)

            logs = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

            if result.returncode != 0:
                return {"status": "FAILED", "logs": logs}

        except Exception as e:
            return {"status": "FAILED", "logs": f"Build process error: {str(e)}"}

        # 4. Find and Move APK
        try:
            apk_path = None
            if stack == "native":
                # Typical Gradle output path
                search_paths = [
                    tmp_path / "app/build/outputs/apk/debug",
                    tmp_path / "build/outputs/apk/debug"
                ]
                for p in search_paths:
                    if p.exists():
                        apks = list(p.glob("*.apk"))
                        if apks:
                            apk_path = apks[0]
                            break
            else:
                # Buildozer typically puts it in bin/
                bin_path = tmp_path / "bin"
                if bin_path.exists():
                    apks = list(bin_path.glob("*.apk"))
                    if apks:
                        apk_path = apks[0]

            if not apk_path:
                return {"status": "FAILED", "logs": f"Build finished but APK not found.\n{logs}"}

            dest_path = STORAGE_DIR / f"{task_id}.apk"
            shutil.move(str(apk_path), str(dest_path))

            return {
                "status": "SUCCESS",
                "logs": logs,
                "download_url": f"/api/v1/download/{task_id}"
            }

        except Exception as e:
            return {"status": "FAILED", "logs": f"Post-processing error: {str(e)}\n{logs}"}

@celery_app.task(bind=True)
def build_apk_task(self, repo_url: str):
    return _build_apk_logic(self, repo_url)
