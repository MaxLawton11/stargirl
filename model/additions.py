import os.path

def loadLog(file_location:str) :
  # gate claues to see if file is real
  if !os.path.isfile(file_location) :
    raise Exception("Log file not found.")
    
  log = json.load(open(file_location))
  return log['max_sequence_length'], log['batch_size']
