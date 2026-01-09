"""WSGI entry point for Gunicorn and other production servers"""

import os
import logging
from pathlib import Path

# Setup path
import sys
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Import and create the Flask app
from web.app import app

# Set production environment
os.environ.setdefault('FLASK_ENV', 'production')

if __name__ == "__main__":
    # This is for direct execution, normally use gunicorn
    app.run()
