import json

# convert into JSON:
log = json.load(open('working_scrips/log.json')) # cuz this is not root we need teh folder idfk

for c in log :
    print(f"{c} - {log[c]}")

with open("working_scrips/new_log.json", "w") as log_output_file:
    new_log_contents = {
        "epochs": 5, 
        "max_sequence_length": 20,
        "batch_size": 64
        }
json.dump(new_log_contents, log_output_file, indent=2) # save file