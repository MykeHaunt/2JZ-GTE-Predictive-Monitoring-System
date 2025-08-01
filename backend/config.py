import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")
    LOG_FILE = os.getenv("LOG_FILE", "logs/backend.log")