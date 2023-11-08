import tensorflow as tf
from tensorflow.keras.metrics import SparseCategoricalAccuracy 
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
import pandas as pd
import pickle
import json

import additions

# tokenize text data
data = pd.read_csv('data/dataset.csv')
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['QUESTIONS'] + data['ANSWERS'])

# save the tokenizer
with open('instances/tokenizer.pkl', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

max_sequence_length = 100
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 128
units = 256

# Encoder
encoder_inputs = tf.keras.layers.Input(shape=(max_sequence_length,))
encoder_embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim)(encoder_inputs)
encoder_lstm = tf.keras.layers.LSTM(units, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(encoder_embedding)
encoder_states = [state_h, state_c]

# Decoder
decoder_inputs = tf.keras.layers.Input(shape=(max_sequence_length,))
decoder_embedding_layer = tf.keras.layers.Embedding(vocab_size, embedding_dim)
decoder_embedding = decoder_embedding_layer(decoder_inputs)
decoder_lstm = tf.keras.layers.LSTM(units, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = tf.keras.layers.Dense(vocab_size, activation='softmax')
output = decoder_dense(decoder_outputs)

# model
model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output)

# compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy', SparseCategoricalAccuracy()])

# save files
model.save('instances/model.keras')
additions.setLog("instances/log.json", 0, max_sequence_length)
    
print("-- Model Created --")
