"""
Optional CAN bus ingestion using python-can
Intended for direct CAN-to-USB interfaces (e.g., Kvaser, CANtact)
"""

import can
import logging

class CANReader:
    def __init__(self, channel='can0', bustype='socketcan'):
        self.channel = channel
        self.bustype = bustype
        self.logger = logging.getLogger(__name__)
        self.bus = None

    def connect(self):
        try:
            self.bus = can.interface.Bus(channel=self.channel, bustype=self.bustype)
            self.logger.info(f"Connected to CAN bus on {self.channel}")
        except Exception as e:
            self.logger.error(f"CAN connection error: {e}")
            self.bus = None

    def read_frame(self):
        if not self.bus:
            return None
        try:
            msg = self.bus.recv(timeout=1)
            return msg
        except Exception as e:
            self.logger.warning(f"CAN read error: {e}")
            return None

    def close(self):
        if self.bus:
            self.bus.shutdown()