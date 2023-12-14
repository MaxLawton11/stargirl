# don't use
# should be deleted
# but after im done

import argparse
import tensorflow as tf

from transformer import model
from transformer.dataset import get_dataset, preprocess_sentence

# um what does this do...
class CustomSchedule(tf.keras.optimizers.schedules.LearningRateSchedule):
    def __init__(self, d_model: int, warmup_steps: int = 4000):
        super(CustomSchedule, self).__init__()
        self.d_model = tf.cast(d_model, dtype=tf.float32)
        self.warmup_steps = warmup_steps

    def __call__(self, step):
        arg1 = tf.math.rsqrt(step)
        arg2 = step * self.warmup_steps**-1.5
        return tf.math.rsqrt(self.d_model) * tf.math.minimum(arg1, arg2)


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


def main(hparams):
    tf.keras.utils.set_random_seed(1234)

    dataset, tokenizer = get_dataset(hparams)

    chatbot = model.transformer(hparams)

    optimizer = tf.keras.optimizers.Adam(
        CustomSchedule(d_model=hparams.d_model), beta_1=0.9, beta_2=0.98, epsilon=1e-9
    )

    cross_entropy = tf.keras.losses.SparseCategoricalCrossentropy(
        from_logits=True, reduction="none"
    )

    def loss_function(y_true, y_pred):
        y_true = tf.reshape(y_true, shape=(-1, hparams.max_length - 1))
        loss = cross_entropy(y_true, y_pred)
        mask = tf.cast(tf.not_equal(y_true, 0), dtype=tf.float32)
        loss = tf.multiply(loss, mask)
        return tf.reduce_mean(loss)

    def accuracy(y_true, y_pred):
        y_true = tf.reshape(y_true, shape=(-1, hparams.max_length - 1))
        return tf.keras.metrics.sparse_categorical_accuracy(y_true, y_pred)

    chatbot.compile(optimizer, loss=loss_function, metrics=[accuracy])

    chatbot.fit(dataset, epochs=hparams.epochs)

    print(f"\nsaving model to {hparams.save_model}...")
    tf.keras.models.save_model(
        chatbot, filepath=hparams.save_model, include_optimizer=False
    )

    print(f"\nclear TensorFlow backend session and load model from {hparams.save_model}...")
    del chatbot
    
    tf.keras.backend.clear_session()
    chatbot = tf.keras.models.load_model(
        hparams.save_model,
        custom_objects={
            "PositionalEncoding": model.PositionalEncoding,
            "MultiHeadAttentionLayer": model.MultiHeadAttentionLayer,
        },
        compile=False,
    )
    evaluate(hparams, chatbot, tokenizer)


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
        epochs=2
        )
    
    main(args)
