# backend/schemas/input_schema.py

def validate_input(data: dict):
    required_fields = {
        "rpm": int,
        "boost": float,
        "afr": float,
        "oil_temp": float,
        "coolant_temp": float,
        "knock": float
    }

    errors = {}
    for field, field_type in required_fields.items():
        if field not in data:
            errors[field] = "Missing"
        else:
            try:
                field_type(data[field])
            except (ValueError, TypeError):
                errors[field] = f"Expected {field_type.__name__}"
    
    return errors