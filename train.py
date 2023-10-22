import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import nltk

nltk.download('punkt')

# Load your dataset
data = pd.read_csv('dataset.csv')

# Tokenize the text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['QUESTIONS'] + data['ANSWERS'])

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
model.fit([input_sequences, output_sequences], \
    np.expand_dims(output_sequences, -1),
    epochs=5,
    batch_size=64
    )

# Inference function
def chatbot_response(input_text):
    input_seq = tokenizer.texts_to_sequences([input_text])
    input_seq = pad_sequences(input_seq, maxlen=max_sequence_length, padding='post')
    predicted_output_seq = model.predict([input_seq, input_seq])
    predicted_output_seq = np.argmax(predicted_output_seq, axis=-1)
    response = ""
    for word_index in predicted_output_seq[0]:
        if word_index == 0:
            break
        word = tokenizer.index_word[word_index]
        response += word + " "
    return response.strip()

# Example usage
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chatbot_response(user_input)
    print("Chatbot:", response)
