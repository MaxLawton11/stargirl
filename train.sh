#!/bin/bash

if test -f instances/tokenizer.pkl; then
  echo "No model found. Creating new model..."
  python3 model/create.py
else
  echo "Model found. Skipping creation."
fi

echo "Training the model..."
python3 model/train.py
