#!/bin/bash
if test -f /instances/tokenizer.pkl; then
  echo "No model found. Creating new model..."
  python3 model/create.py
fi
python3 model/train.py
