# backend/validation/schemas.py

from pydantic import BaseModel, Field, conint, confloat

class SensorData(BaseModel):
    rpm: conint(ge=0, le=15000)
    boost: confloat(ge=-15.0, le=50.0)  # psi
    afr: confloat(ge=5.0, le=25.0)
    oil_temp: conint(ge=-40, le=180)   # °C
    coolant_temp: conint(ge=-40, le=150)  # °C
    knock: confloat(ge=0.0, le=100.0)