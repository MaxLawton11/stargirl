#!/bin/bash
if test -f instances/tokenizer.pkl; then
  if test -f instances/model.keras; then
    echo "No model found. Creating new model..."
    python3 model/create.py
  fi
fi
python3 model/train.py