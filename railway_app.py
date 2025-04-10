from flask import Flask, jsonify
import os
import logging
import sys

# Setup logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Starting Railway App")

# Create application
app = Flask(__name__)

@app.route('/')
def index():
    logger.info("Root route accessed")
    return jsonify({
        "status": "ok",
        "message": "Railway Deployment is working!"
    })

@app.route('/health')
def health():
    logger.info("Health route accessed")
    return jsonify({
        "status": "healthy"
    })

@app.route('/info')
def info():
    logger.info("Info route accessed")
    env_vars = {k: v for k, v in os.environ.items() 
                if not any(s in k.lower() for s in ['key', 'token', 'secret', 'password'])}
    
    return jsonify({
        "status": "info",
        "python_version": sys.version,
        "environment": env_vars,
        "working_directory": os.getcwd(),
        "files": os.listdir('.')
    })

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Error: {str(e)}", exc_info=True)
    return jsonify({
        "status": "error",
        "message": str(e)
    }), 500

# Debug info on startup
logger.info(f"Python version: {sys.version}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"Directory contents: {os.listdir('.')}")
try:
    logger.info(f"PORT env var: {os.environ.get('PORT')}")
except Exception as e:
    logger.error(f"Error getting PORT: {e}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port) 