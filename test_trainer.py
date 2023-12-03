import json
import model_data

log_filename = 'working_scrips/log.json'

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
    
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-e','--nepochs', help='# of epochs this training cycle', action="store_true")
args = parser.parse_args()
if args.nepochs:
    print(args.nepochs)
    
"""
if __name__ == "__main__":
    
    # training vars
    args = argparse.Namespace(\
        save_model='model.h5', # path save the model
        max_samples=25000, # maximum number of conversation pairs to use
        max_length=40, # maximum sentence length
        batch_size=64, 
        num_layers=2, 
        num_units=512, 
        d_model=256, 
        num_heads=8, 
        dropout=0.1, 
        activation='relu', 
        epochs=20
        )
    
    main(args)
"""