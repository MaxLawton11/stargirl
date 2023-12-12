import argparse
import tensorflow as tf

from model_data import model
from model_data.dataset import get_dataset, preprocess_sentence

from model_data.import evaluation_functions

class Model():
    def __init__(self, hparams):
        self.hparams = hparams
        self.dataset, self.tokenizer = get_dataset(hparams)
        
    def _loadModel(self) :
        tf.keras.backend.clear_session()
        chatbot = tf.keras.models.load_model(
            self.hparams.save_model,
            custom_objects={
                "PositionalEncoding": model.PositionalEncoding,
                "MultiHeadAttentionLayer": model.MultiHeadAttentionLayer,
            },
            compile=False,
        )
        return chatbot
        
        
    def train(self, epochs) :
        chatbot = self._loadModel()
        
        chatbot.fit(self.dataset, epochs=epochs)
        
        tf.keras.models.save_model(
            chatbot, filepath=self.hparams.save_model, include_optimizer=False
        )
        del chatbot
        
    def evaluate(self) :
        chatbot = self._loadModel()
        return evaluation_functions.evaluate(self.hparams, chatbot, self.tokenizer)
        
