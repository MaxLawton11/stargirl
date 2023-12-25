import argparse
import tensorflow as tf
import os.path

from model_data.transformer import model
from model_data.transformer.dataset import get_dataset, preprocess_sentence

from model_data import evaluation_functions

class Model():
    def __init__(self, hparams):
        self.hparams = hparams
        self.dataset, self.tokenizer = get_dataset(hparams)
        
        
    def _testVaildModel(self) :
        return os.path.isfile(self.hparams.save_model)
    
    def _loadModel(self) :
        if self._testVaildModel() :
            tf.keras.backend.clear_session()
            chatbot = tf.keras.models.load_model(
                self.hparams.save_model,
                custom_objects={
                    "PositionalEncoding": model.PositionalEncoding,
                    "MultiHeadAttentionLayer": model.MultiHeadAttentionLayer,
                }, compile=False, )
            return chatbot
        else :
            raise Exception("No vaild model!")
        
    def createModel(self) :
        pass
        
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
        
