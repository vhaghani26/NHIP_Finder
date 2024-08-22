#!/usr/bin/env python3

'''
python3 01_read_samples.py --data_dir 01_raw_data/
'''

import argparse
import os
import sys

#####################
## Set Up Argparse ##
#####################

# Initialize argparse
parser = argparse.ArgumentParser(
    description='Extract samples names from fastq files')

parser.add_argument('--data_dir', required=True, type=str,
    metavar='<str>', help='Directory containing the fastq files')
    
# Finalization of argparse
arg = parser.parse_args()

##########################
## Extract Sample Names ## 
##########################

# Initiate empty list to store sample names
samples = []

# Extract

for file_name in os.listdir(arg.data_dir):
    if file_name.endswith('fastq.gz'):
        base_name = file_name.replace('.fastq.gz', '')
        samples.append(base_name)
    elif file_name.endswith('fq.gz'):
        base_name = file_name.replace('.fq.gz', '')
        samples.append(base_name)
        
#########################
## Create samples.yaml ##
#########################

# Create samples.yaml 
print("Creating samples.yaml, which will contain all unique sample IDs and get used in further analysis.")
file = "samples.yaml"
os.system(f"touch {file}")

# Saving reference of standard output
original_stdout = sys.stdout

# Write sample IDs into task_samples.yaml
with open(file, "a") as f:
    sys.stdout = f
    print("---")
    print(f"sequence_data: {arg.data_dir}")
    print("samples:")
    for samp in samples:
        print(f"  - {samp}")
    
# Reset standard output
sys.stdout = original_stdout
print("samples.yaml has been created.")
