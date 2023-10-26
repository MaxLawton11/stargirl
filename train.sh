#!/bin/bash

if instances/tokenizer.pkl; then
  echo "\$ Didn't find 'tokenizer.pkl'. Creating new model..."
  python3 model/create.py
fi

echo "\$ Training the model..."
python3 model/train.py
