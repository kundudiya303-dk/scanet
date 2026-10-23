"""Cross-working-directory smoke tests for the application runtime."""
import os
import sys
import tempfile


def test_app_starts_and_serves_files_outside_project_directory():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(project_root, "backend")
    original_cwd = os.getcwd()
    sys.path.insert(0, backend_dir)

    try:
        with tempfile.TemporaryDirectory() as working_directory:
            os.chdir(working_directory)
            try:
                from fastapi.testclient import TestClient
                from main import app

                with TestClient(app) as client:
                    assert client.get("/").status_code == 200
                    assert client.get("/assets/css/main.css").status_code == 200
                    assert client.get("/api/v1/system/health").json()["status"] == "ok"
            finally:
                os.chdir(original_cwd)
    finally:
        sys.path.remove(backend_dir)
