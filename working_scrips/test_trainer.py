import json
import model

log_filename = 'working_scrips/log.json'
run_nepochs = 1

# convert into JSON:
log = json.load(open(log_filename)) # cuz this is not root we need teh folder idfk

try:
    # try to train run_nepochs's
    pass
    # increse epoch in log
    log['epochs'] += 2
except :
    # DO NOT CHANGE LOG
    pass

# print new contets to file
with open(log_filename, 'w') as log_output_file:
    new_log_contents = {
        "model_filename" : log['model_filename'],
        "epochs": log['epochs'], 
        "max_sequence_length": log['max_sequence_length'],
        "batch_size": log['batch_size']
    }
    json.dump(new_log_contents, log_output_file, indent=2) # save file