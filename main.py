from app import app
import subprocess
import os
import sys
import signal
import atexit

# Flet process management
flet_process = None

def start_flet_app():
    """Start the Flet application in a separate process"""
    global flet_process
    if flet_process is None or flet_process.poll() is not None:
        # Start the Flet app on port 8080
        try:
            flet_process = subprocess.Popen(
                [sys.executable, "run.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"Started Flet application (PID: {flet_process.pid})")
            return True
        except Exception as e:
            print(f"Error starting Flet app: {e}")
            return False
    return True

def stop_flet_app():
    """Stop the Flet application process"""
    global flet_process
    if flet_process is not None and flet_process.poll() is None:
        try:
            flet_process.terminate()
            flet_process.wait(timeout=5)
            print("Stopped Flet application")
        except:
            flet_process.kill()
            print("Killed Flet application")

# Register clean up function
atexit.register(stop_flet_app)

# Add route to start the Flet app
@app.route('/run-flet')
def run_flet():
    """Run the Flet application"""
    success = start_flet_app()
    if success:
        return {"status": "ok", "message": "Flet application started successfully"}
    else:
        return {"status": "error", "message": "Failed to start Flet application"}, 500

if __name__ == '__main__':
    # Try to start the Flet app when the Flask app starts
    start_flet_app()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)