import argparse
import tensorflow as tf

import evaluation_functions

class Model():
    def __init__(self, *args):
        self.dataset, self.tokenizer = get_dataset(hparams)
        
    def evaluate(self, hparams) :
        tf.keras.backend.clear_session()
        chatbot = tf.keras.models.load_model(
            hparams.save_model,
            custom_objects={
                "PositionalEncoding": model.PositionalEncoding,
                "MultiHeadAttentionLayer": model.MultiHeadAttentionLayer,
            },
            compile=False,
        )
        evaluation_functions.evaluate(hparams, chatbot, self.tokenizer)
        