import json

log_filename = 'working_scrips/log.json'
run_nepochs = 1

# convert into JSON:
log = json.load(open(log_filename)) # cuz this is not root we need teh folder idfk

for c in log :
    print(f"{c} - {log[c]}")

# print new files
with open(log_filename, 'w') as log_output_file:
    new_log_contents = {
        "model_filename" : log['model_filename'],
        "epochs": log['epochs'], 
        "max_sequence_length": log['max_sequence_length'],
        "batch_size": log['batch_size']
        }
    json.dump(new_log_contents, log_output_file, indent=2) # save file