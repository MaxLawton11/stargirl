#!/bin/bash
if test -f instances/tokenizer.pkl; then
  echo "File exists."
fi
python3 model/train.py