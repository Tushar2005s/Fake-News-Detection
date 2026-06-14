import subprocess

# Start Flask server (app.py)
flask_process = subprocess.Popen(["python", "app.py"])

# Start FastAPI server (backend_real_time.py)
fastapi_process = subprocess.Popen(["python", "backend_real_time.py"])

# Wait for both processes to complete
flask_process.wait()
fastapi_process.wait()
