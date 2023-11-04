#!/bin/bash

echo "\$ Installing dependencies..."
pip3 install sqlite3
pip3 install pandas
pip3 install numpy
pip3 install tensorflow
pip3 install pickle

echo "\$ Setting up dataset..."
python3 data/extraction.py
