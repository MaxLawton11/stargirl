import os.path
import json

def loadLog(file_location:str) :
  # gate claues to see if file is real
  if not os.path.isfile(file_location) :
    raise Exception("Log file not found.")
  log = json.load(open(file_location))
  return log['epochs'], log['max_sequence_length'], log['batch_size']

def setLog(file_location:str, epochs, max_sequence_length) :
  # open log file (will create new one if not found)
  with open(file_location, "w") as log_file:
      new_log = {
          "epochs": 0,
          "max_sequence_length": max_sequence_length,
          "batch_size": 64
      }
      json.dump(new_log, log_file, indent=2) # save file
