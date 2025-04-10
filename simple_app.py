from flask import Flask
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Starting simple Flask app")

# Create Flask app
app = Flask(__name__)

@app.route('/')
def index():
    logger.info("Root route accessed")
    return "Hello from Railway! Simple Flask app is working."

@app.route('/health')
def health():
    logger.info("Health route accessed")
    return "OK"

if __name__ == '__main__':
    # Get port from environment variable
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting app on port {port}")
    
    # Print environment info
    logger.info(f"Python environment: {os.environ.get('PYTHON_VERSION', 'unknown')}")
    logger.info(f"Environment variables: {[k for k in os.environ.keys() if not any(s in k.lower() for s in ['key', 'token', 'password'])]}")
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True) 