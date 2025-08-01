import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

class Config:
    # ========== General ==========
    BASE_DIR = Path(__file__).resolve().parent.parent

    # ========== Logging ==========
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", str(BASE_DIR / "logs/backend.log"))

    # ========== ML Model ==========
    MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "model/model.pkl"))
    MODEL_TYPE = os.getenv("MODEL_TYPE", "random_forest")

    # ========== Sensor Ingestion ==========
    SENSOR_MODE = os.getenv("SENSOR_MODE", "OBD").upper()  # OBD or CAN
    OBD_PORT = os.getenv("OBD_PORT", "/dev/ttyUSB0")       # Serial port for ELM327
    OBD_BAUDRATE = int(os.getenv("OBD_BAUDRATE", "9600"))
    OBD_TIMEOUT = float(os.getenv("OBD_TIMEOUT", "1"))

    CAN_INTERFACE = os.getenv("CAN_INTERFACE", "can0")     # e.g., can0
    CAN_BUSTYPE = os.getenv("CAN_BUSTYPE", "socketcan")    # socketcan, slcan, etc.

    # ========== Flask Server ==========
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = FLASK_ENV == "development"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))

    # ========== Security ==========
    SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-default-key")  # should be overridden in prod

    # ========== Miscellaneous ==========
    TIMEZONE = os.getenv("TZ", "Asia/Dhaka")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")  # for CORS

    @classmethod
    def summary(cls):
        return {
            "MODEL_PATH": cls.MODEL_PATH,
            "LOG_FILE": cls.LOG_FILE,
            "SENSOR_MODE": cls.SENSOR_MODE,
            "OBD_PORT": cls.OBD_PORT,
            "CAN_INTERFACE": cls.CAN_INTERFACE,
            "FLASK_ENV": cls.FLASK_ENV,
        }

# For testing/debugging
if __name__ == "__main__":
    import pprint
    pprint.pprint(Config.summary())