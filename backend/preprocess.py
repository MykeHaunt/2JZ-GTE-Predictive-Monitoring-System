import numpy as np

def preprocess_input(data_dict):
    # Assume keys: rpm, boost, afr, oil_temp, coolant_temp, knock
    features = [
        float(data_dict.get("rpm", 0)),
        float(data_dict.get("boost", 0)),
        float(data_dict.get("afr", 14.7)),
        float(data_dict.get("oil_temp", 85)),
        float(data_dict.get("coolant_temp", 90)),
        float(data_dict.get("knock", 0)),
    ]
    return np.array(features)