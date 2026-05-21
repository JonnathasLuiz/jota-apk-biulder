import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from app.tasks import _build_apk_logic

@patch("app.tasks.Repo.clone_from")
@patch("app.tasks.subprocess.run")
@patch("app.tasks.shutil.move")
def test_build_apk_task_native_success(mock_move, mock_run, mock_clone):
    # Mock subprocess run
    mock_run_result = MagicMock()
    mock_run_result.returncode = 0
    mock_run_result.stdout = "Build successful"
    mock_run_result.stderr = ""
    mock_run.return_value = mock_run_result

    with patch("pathlib.Path.exists") as mock_exists:
        with patch("pathlib.Path.glob") as mock_glob:
            # Mock detection: build.gradle exists
            def exists_side_effect():
                return True
            mock_exists.side_effect = exists_side_effect

            # Mock finding APK
            mock_apk = MagicMock()
            mock_apk.__str__.return_value = "/tmp/fake/app/build/outputs/apk/debug/app-debug.apk"
            mock_glob.return_value = [mock_apk]

            # Call logic directly
            result = _build_apk_logic(None, "https://github.com/user/native-repo.git")

            if result["status"] == "FAILED":
                print(f"DEBUG: {result['logs']}")

            assert result["status"] == "SUCCESS"
            assert "download_url" in result
            mock_clone.assert_called_once()
            mock_run.assert_called()

@patch("app.tasks.Repo.clone_from")
def test_build_apk_task_clone_fail(mock_clone):
    mock_clone.side_effect = Exception("Clone error")

    result = _build_apk_logic(None, "https://github.com/user/bad-repo.git")

    assert result["status"] == "FAILED"
    assert "Clone error" in result["logs"]
