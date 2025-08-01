import os
import pytest
from backend.model import train_model, validate_model

@pytest.fixture
def sample_data_path():
    return "data/engine_data.csv"

def test_training_pipeline(sample_data_path):
    model_out = "model/test_model.pkl"
    train_model.train_and_save_model(sample_data_path, model_out)
    assert os.path.exists(model_out)

def test_validation_pipeline(sample_data_path):
    model_out = "model/test_model.pkl"
    report = validate_model.validate_model(model_out, sample_data_path)
    assert "accuracy" in report