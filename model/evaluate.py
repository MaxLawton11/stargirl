import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.metrics import SparseCategoricalAccuracy 
import numpy as np
import pandas as pd
import pickle
import json

log = json.load(open('instances/log.json'))

max_sequence_length = log['max_sequence_length']

# Load the tokenizer (assuming it's saved along with the model)
with open('instances/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the model
model = tf.keras.models.load_model('instances/model.keras')
    
# Inference function
def response(input_text):
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
    response = response(user_input)
    print("Response:", response)

