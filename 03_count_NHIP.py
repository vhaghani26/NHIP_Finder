#!/usr/bin/env python3

'''
Usage:
python3 03_count_NHIP.py --in_dir 04_NHIP_count/ --out_dir .
'''

####################
## Import Modules ##
####################

import argparse
import os
import pandas as pd
import re

#####################
## Set Up Argparse ##
#####################

# Initialize argparse
parser = argparse.ArgumentParser(
    description='Count NHIP reads detected in samples')

parser.add_argument('--in_dir', required=True, type=str,
    metavar='<str>', help='Directory containing the files with the NHIP counts in it (04_NHIP_count/)')

parser.add_argument('--out_dir', required=True, type=str,
    metavar='<str>', help='Directory to output NHIP count CSV file')

# Finalization of argparse
arg = parser.parse_args()

######################
## Count NHIP Reads ##
######################

# Initialize dictionary for storing values
data = {}

# Iterate over each file in the directory
for filename in os.listdir(arg.in_dir):
    # Construct the full file path
    filepath = os.path.join(arg.in_dir, filename)
    
    # Check if it is a file (not a directory) and if it ends with "_hg38.txt"
    if os.path.isfile(filepath) and filename.endswith("_hg38.txt"):
        # Extract sample name from the filename
        match = re.match(r"(.*)_hg38\.txt", filename)
        if match:
            sample = match.group(1)
            
            # Open the file and read its content
            with open(filepath, 'r') as file:
                value = file.read().strip()
                
                # Initialize dictionary entry if the sample doesn't exist yet
                if sample not in data:
                    data[sample] = {"Sample": sample, "NHIP_Counts": ""}
                
                # Assign the value to the hg38 category
                data[sample]["NHIP_Counts"] = value

# Convert the dictionary to a DataFrame
df = pd.DataFrame.from_dict(data, orient='index')

# Sort the dataframe by sample name
df = df.sort_values(by='Sample')

# Save the dataframe as a CSV
output_path = os.path.join(arg.out_dir, 'NHIP_counts.csv')
df.to_csv(output_path, index=False)
