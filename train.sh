#!/bin/bash

# List all files in the 'instances' directory for debugging
echo "Files in 'instances' directory:"
ls instances

# Check for the specific file 'tokenizer.pkl'
if [[ -f instances/tokenizer.pkl ]]; then
  echo "Found tokenizer.pkl. Creating new model..."
  python3 model/create.py
else
  echo "No tokenizer.pkl found. Skipping model creation."
fi

echo "Training the model..."
python3 model/train.py
