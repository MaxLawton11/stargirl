import argparse
import tensorflow as tf

from transformer import model
from transformer.dataset import get_dataset, preprocess_sentence

import evaluation_functions

class Model():
    def __init__(self, hparams):
        self.hparams = hparams
        self.dataset, self.tokenizer = get_dataset(hparams)
        
    def train(self, epochs) :
        tf.keras.backend.clear_session()
        chatbot = tf.keras.models.load_model(
            self.hparams.save_model,
            custom_objects={
                "PositionalEncoding": model.PositionalEncoding,
                "MultiHeadAttentionLayer": model.MultiHeadAttentionLayer,
            },
            compile=False,
        )
        
        chatbot.fit(self.dataset, epochs=epochs)
        
        tf.keras.models.save_model(
            chatbot, filepath=self.hparams.save_model, include_optimizer=False
        )
        del chatbot
        
    def evaluate(self) :
        tf.keras.backend.clear_session()
        chatbot = tf.keras.models.load_model(
            self.hparams.save_model,
            custom_objects={
                "PositionalEncoding": model.PositionalEncoding,
                "MultiHeadAttentionLayer": model.MultiHeadAttentionLayer,
            },
            compile=False,
        )
        evaluation_functions.evaluate(self.hparams, chatbot, self.tokenizer)
        