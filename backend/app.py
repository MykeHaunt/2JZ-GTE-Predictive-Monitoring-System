from flask import Flask
from routes import api_blueprint
from logger import setup_logger
import config

app = Flask(__name__)
app.config.from_object(config.Config)

# Setup logger
logger = setup_logger()

# Register API routes
app.register_blueprint(api_blueprint, url_prefix="/api")

if __name__ == "__main__":
    logger.info("Starting 2JZ-GTE Predictive Monitoring API...")
    app.run(debug=True, host='0.0.0.0', port=5000)