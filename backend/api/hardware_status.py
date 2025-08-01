# backend/api/hardware_status.py

import random

class HardwareStatus:
    @staticmethod
    def get_status():
        return {
            "OBD_Connection": random.choice(["Connected", "Disconnected"]),
            "CAN_Bus_Status": random.choice(["Active", "Inactive"]),
            "Sensor_Status": {
                "RPM": "OK",
                "Boost": "OK",
                "AFR": "OK",
                "OilTemp": "OK",
                "CoolantTemp": "OK",
                "Knock": "OK"
            }
        }