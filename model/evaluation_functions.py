import argparse
import tensorflow as tf

from transformer import model
from transformer.dataset import get_dataset, preprocess_sentence

# used for telling what the chatbot says
def inference(hparams, chatbot, tokenizer, sentence):
    sentence = preprocess_sentence(sentence)

    sentence = tf.expand_dims(
        hparams.start_token + tokenizer.encode(sentence) + hparams.end_token, axis=0
    )

    output = tf.expand_dims(hparams.start_token, 0)

    for i in range(hparams.max_length):
        predictions = chatbot(inputs=[sentence, output], training=False)

        # select the last word from the seq_len dimension
        predictions = predictions[:, -1:, :]
        predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

        # return the result if the predicted_id is equal to the end token
        if tf.equal(predicted_id, hparams.end_token[0]):
            break

        # concatenated the predicted_id to the output which is given to the decoder as its input.
        output = tf.concat([output, predicted_id], axis=-1)

    return tf.squeeze(output, axis=0)

# gen cont.
def predict(hparams, chatbot, tokenizer, sentence):
    prediction = inference(hparams, chatbot, tokenizer, sentence)
    predicted_sentence = tokenizer.decode(
        [i for i in prediction if i < tokenizer.vocab_size]
    )
    return predicted_sentence

# gen cont..
def evaluate(hparams, chatbot, tokenizer):
    print("\nEvaluate")
    sentence = "where have you been?"
    output = predict(hparams, chatbot, tokenizer, sentence)
    print(f"input: {sentence}\noutput: {output}")

    sentence = "it's a trap!"
    output = predict(hparams, chatbot, tokenizer, sentence)
    print(f"\ninput: {sentence}\noutput: {output}")

    sentence = "I am not crazy, my mother had me tested"
    for _ in range(5):
        output = predict(hparams, chatbot, tokenizer, sentence)
        print(f"\ninput: {sentence}\noutput: {output}")
        sentence = output


"""
if __name__ == "__main__":
    
    # training vars
    args = argparse.Namespace(\
        save_model='model.h5', # path save the model
        max_samples=25000, # maximum number of conversation pairs to use
        max_length=40, # maximum sentence length
        batch_size=64, 
        num_layers=2, 
        num_units=512, 
        d_model=256, 
        num_heads=8, 
        dropout=0.1, 
        activation='relu', 
        epochs=20
        )
    
    main(args)
"""