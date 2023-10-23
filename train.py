import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import pickle
import nltk

nltk.download('punkt')

# Load your dataset
data = pd.read_csv('dataset.csv')

# Tokenize the text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['QUESTIONS'] + data['ANSWERS'])

# Save the tokenizer
with open('tokenizer.pkl', 'wb') as handle:
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

# Model
model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output)

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
# we are traing with a loop cuz somtimes the computer shits the bed
n_epochs = 25
for _ in range(n_epochs) :
    model.fit([input_sequences, output_sequences], \
        np.expand_dims(output_sequences, -1),
        epochs=1,
        batch_size=64
        )
    model.save('chatbot_model.h5')

# After training, save the model
print("-- Model Trained --")

