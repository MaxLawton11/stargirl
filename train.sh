#!/bin/bash

# List all files in the 'instances' directory
echo "Files in 'instances' directory:"
ls instances

if test -f instances/tokenizer.pkl; then
  echo "No model found. Creating new model..."
  python3 model/create.py
fi

echo "Training the model..."
python3 model/train.py
