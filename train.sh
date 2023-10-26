#!/bin/bash

if ! -f instances/tokenizer.pkl; then
  if ! -f instances/model.keras; then
    echo "\$ Didn't find 'tokenizer.pkl'. Creating new model..."
    python3 model/create.py
  fi
fi

echo "\$ Training the model..."
python3 model/train.py
