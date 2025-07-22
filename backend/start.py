#!/usr/bin/env python3
"""
Startup script for the Stock Prediction Flask API
"""
import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_requirements():
    """Install required Python packages"""
    try:
        logger.info("Installing Python requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install requirements: {e}")
        return False

def start_flask_app():
    """Start the Flask application"""
    try:
        logger.info("Starting Flask application...")
        from app import app
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting Stock Prediction API...")
    
    # Install requirements if needed
    if "--install" in sys.argv or not os.path.exists("venv"):
        if not install_requirements():
            sys.exit(1)
    
    # Start the Flask app
    start_flask_app()
