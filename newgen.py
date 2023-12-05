import argparse
import json

from model_data import Model

log = json.load(open('log.json'))

chatbot = Model(
    # make a way to make sure this is always the same
    argparse.Namespace(\
        save_model=log['model_filename'], # path save the model
        max_samples=25000, # maximum number of conversation pairs to use
        max_length=40, # maximum sentence length
        batch_size=64, 
        num_layers=2, 
        num_units=512, 
        d_model=256, 
        num_heads=8, 
        dropout=0.1, 
        activation='relu', 
        epochs=log['epochs']
        )
)

chatbot.evaluate()
