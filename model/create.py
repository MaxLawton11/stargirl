import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import pickle
import json

# i don't think these are used at all...
#import nltk
#nltk.download('punkt')

# load dataset
data = pd.read_csv('data/dataset.csv')

# tokenize text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['QUESTIONS'] + data['ANSWERS'])

# save the tokenizer
with open('instances/tokenizer.pkl', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Convert text to sequences
input_sequences = tokenizer.texts_to_sequences(data['QUESTIONS'])
output_sequences = tokenizer.texts_to_sequences(data['ANSWERS'])

# Pad sequences for consistent input length
max_sequence_length = 20
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='post')
output_sequences = pad_sequences(output_sequences, maxlen=max_sequence_length, padding='post')

# Vocabulary size
vocab_size = len(tokenizer.word_index) + 1

# Build the model
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
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# save file
model.save('instances/model.keras')

log = {
  "epochs": 0,
  "max_sequence_length": max_sequence_length,
  "batch_size": 64,
  "model_file_name": "instances/model.h5",
  "tokenizer_file_name": "instances/tokenizer.plk"
  }

with open("instances/log.json", "w") as log_file:
    json.dump(log, log_file, indent=4)