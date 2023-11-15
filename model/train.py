import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import pickle

import additions 

current_epochs, max_sequence_length, batch_size = additions.loadLog('instances/log.json')

# Load the tokenizer (assuming it's saved along with the model)
with open('instances/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the model
model = tf.keras.models.load_model('instances/model.keras')

# Convert data to sequences
data = pd.read_csv('data/dataset.csv')
input_sequences = tokenizer.texts_to_sequences(data['QUESTIONS'])
output_sequences = tokenizer.texts_to_sequences(data['ANSWERS'])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='post')
output_sequences = pad_sequences(output_sequences, maxlen=max_sequence_length, padding='post')

print(f"-- Starting on epoch {current_epochs}")

# Train the model
n_epochs = 1
model.fit([input_sequences, output_sequences], np.expand_dims(output_sequences, -1), epochs=n_epochs, batch_size=batch_size )

#save files
model.save('instances/model.keras')
additions.setLog("instances/log.json", current_epochs+n_epochs, max_sequence_length)
    
print(f"-- Model Trained ({n_epochs} epochs) --")
