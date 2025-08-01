import threading
from datetime import datetime

class SystemStatus:
    _lock = threading.Lock()
    _status = {
        "obd_connected": False,
        "can_active": False,
        "hardware_ingestion": False,
        "simulated_ingestion": False,
        "last_update": None,
        "latest_data": None,
    }

    @classmethod
    def update_status(cls, key, value):
        with cls._lock:
            cls._status[key] = value
            if key in ["latest_data", "last_update"]:
                return
            cls._status["last_update"] = datetime.utcnow().isoformat()

    @classmethod
    def update_latest_data(cls, data):
        with cls._lock:
            cls._status["latest_data"] = data
            cls._status["last_update"] = datetime.utcnow().isoformat()

    @classmethod
    def get_status(cls):
        with cls._lock:
            return dict(cls._status)