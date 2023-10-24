import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd
import pickle
import json

log = json.load(open('instances/log.json'))

max_sequence_length = log['max_sequence_length']
batch_size = log['max_sequence_length']

# Load the tokenizer (assuming it's saved along with the model)
with open('instances/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Convert data to sequences
data = pd.read_csv('data/dataset.csv')
input_sequences = tokenizer.texts_to_sequences(data['QUESTIONS'])
output_sequences = tokenizer.texts_to_sequences(data['ANSWERS'])
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='post')
output_sequences = pad_sequences(output_sequences, maxlen=max_sequence_length, padding='post')

# Load the model
model = tf.keras.models.load_model('instances/model.keras')

# Train the model
# we are traing with a loop cuz somtimes the computer shits the bed
n_epochs = 5
model.fit([input_sequences, output_sequences], np.expand_dims(output_sequences, -1), epochs=n_epochs, batch_size=batch_size )

model.save('instances/model.keras')


with open("instances/log.json", "w") as log_file:
    new_log = {
        "epochs": log['epochs']+n_epochs,
        "max_sequence_length": max_sequence_length,
        "batch_size": batch_size
        }
    json.dump(new_log, log_file, indent=2)
    
print(f"-- Model Trained ({n_epochs} epochs) --")
