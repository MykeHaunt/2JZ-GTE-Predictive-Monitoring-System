"""
Dynamic loader for sensor input mode (OBD-II or CAN)
"""

import os
from .obd_connector import OBDConnector
from .can_reader import CANReader

def get_sensor_interface(mode="OBD"):
    mode = mode.upper()
    if mode == "OBD":
        connector = OBDConnector()
        connector.connect()
        return connector
    elif mode == "CAN":
        reader = CANReader()
        reader.connect()
        return reader
    else:
        raise ValueError("Unsupported sensor mode: must be 'OBD' or 'CAN'")