import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Load the tokenizer (assuming it's saved along with the model)
with open('tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the model
model = tf.keras.models.load_model('chatbot_model.h5')

# Max sequence length used during training
max_sequence_length = 20

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
