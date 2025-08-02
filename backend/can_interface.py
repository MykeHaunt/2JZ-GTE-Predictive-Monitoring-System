def parse_can_payload(arbitration_id, payload_bytes):
    spec = CAN_MESSAGE_SPECS.get(arbitration_id)
    if not spec:
        return None  # unknown message type
    try:
        fields = spec.decode(payload_bytes)
        return fields
    except Exception:
        logger.warning(f"Payload parsing failed for ID {arbitration_id}: {payload_bytes.hex()}")
        return None