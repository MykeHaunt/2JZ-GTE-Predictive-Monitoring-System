"""
OBD-II Connector via ELM327 using python-OBD
Supports serial or Bluetooth interfaces
"""

import obd
import logging
from time import sleep

class OBDConnector:
    def __init__(self, port_str=None, baudrate=9600, timeout=1):
        self.connection = None
        self.logger = logging.getLogger(__name__)
        self.port = port_str or obd.scan_serial()[0]  # auto-scan
        self.baudrate = baudrate
        self.timeout = timeout

    def connect(self):
        try:
            self.connection = obd.OBD(portstr=self.port, baudrate=self.baudrate, fast=False, timeout=self.timeout)
            self.logger.info(f"Connected to OBD-II on {self.port}")
        except Exception as e:
            self.logger.error(f"Failed to connect to OBD-II: {e}")

    def read_pid(self, pid_command):
        if not self.connection or not self.connection.is_connected():
            return None
        cmd = getattr(obd.commands, pid_command.upper(), None)
        if not cmd:
            self.logger.warning(f"Invalid PID command: {pid_command}")
            return None
        response = self.connection.query(cmd)
        return response.value if response and response.value else None

    def close(self):
        if self.connection:
            self.connection.close()