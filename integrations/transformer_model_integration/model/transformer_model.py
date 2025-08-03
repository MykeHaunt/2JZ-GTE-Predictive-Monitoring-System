import tensorflow as tf
from tensorflow.keras import layers, Model

def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0.1):
    x = layers.MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout)(inputs, inputs)
    x = layers.Dropout(dropout)(x)
    res = layers.Add()([x, inputs])
    x = layers.Conv1D(ff_dim, 1, activation="relu")(res)
    x = layers.Dropout(dropout)(x)
    x = layers.Conv1D(inputs.shape[-1], 1)(x)
    return layers.Add()([x, res])

def build_transformer(input_shape, head_size, num_heads, ff_dim, num_layers, dropout=0.1):
    inp = layers.Input(shape=input_shape)
    x = inp
    positions = tf.range(start=0, limit=input_shape[0], delta=1)
    pos_emb = layers.Embedding(input_dim=input_shape[0], output_dim=input_shape[1])(positions)
    x = layers.Add()([x, pos_emb])
    for _ in range(num_layers):
        x = transformer_encoder(x, head_size, num_heads, ff_dim, dropout)
    x = layers.GlobalAveragePooling1D()(x)
    out = layers.Dense(input_shape[1])(x)
    return Model(inp, out)