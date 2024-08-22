# NHIP Finder

Collaborators: Viktoria Haghani, Vanessa Su, Jewel Wilson, He Yang

This pipeline is designed to be fed in raw data in the form of FASTQ files (`fq.gz` or `fastq.gz`) and output the number of NHIP reads detected per sample.

## Read in Samples (`01_read_samples.py`)

First, we need to read in the sample names from the sequencing data directory to create the `samples.yaml` file. This `samples.yaml` file will subsequently be used to delineate sample names for Snakemake to use in the alignment, deduplication, and sorting process to enable detection of NHIP.

You will need to link the raw data to your working directory, where you plan on running the pipeline. In your working directory, create a soft link to the original data set. Please use the absolute path (i.e. starting with `/share/lasallelab/`). 

```
# Create a soft link to the original data set
ln -s {absolute_path_to_raw_data} 01_raw_data
```

Next, we will run the script that will extract sample names and store them in the `samples.yaml` file:

```
# Extract sample names to output to samples.yaml
python3 01_read_samples.py --data_dir 01_raw_data/
```

## Snakemake (`02_snakefile`)

This is a snakemake file that indexes the hg38 genome, aligns the sample reads to hg38, sorts, deduplicates, and indexes the data such that Samtools can count the number of reads ultimately aligned to NHIP. The following region was used to detect NHIP:

* hg38: chr22:49043919-49052385

To run this step, run the following in your working directory:

```
# Activate conda environment
conda activate /share/lasallelab/programs/.conda/rocketchip

# Run snakemake 
snakemake -j 5 -s 02_snakefile
```

The final output is a single text file in the directory `04_NHIP_count/` using the notation `{sample}_hg38.txt`. Essentially, there is one file per sample containing the read counts for NHIP. These will be read in during the next step and organized as a CSV file.

### Validation for Counting

In order to validate that this pipeline works as intended, I ran MeCP2 ChIP-seq data through the pipeline and counted the number of reads at BDNF, a known MeCP2 binding site, in the mm10 genome. It successfully output 346 reads for the sample I tested, indicating that the syntax and counting work correctly.

## NHIP Counting (`03_count_NHIP.py`)

Once Snakemake fully finishes running, we have a directory, `04_NHIP_count/` that contains all of the text files storing the number of NHIP  reads detected. To read in the data and store it effectively in a CSV, run the following in your working directory:

```
# Count NHIP reads and output a CSV file
python3 03_count_NHIP.py --in_dir 04_NHIP_count/ --out_dir .
```

The final output of this pipeline is `NHIP_counts.csv`, which contains all of the count data for the input samples.