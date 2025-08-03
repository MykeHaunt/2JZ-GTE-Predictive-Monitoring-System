import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i])
        y.append(data[i])
    return np.array(X), np.array(y)

data = pd.read_csv('data/engine_data.csv')
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

X, y = create_sequences(scaled_data, 60)