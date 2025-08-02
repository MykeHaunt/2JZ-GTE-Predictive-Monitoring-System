import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_home():
    response = app.test_client().get("/")
    assert response.status_code == 200