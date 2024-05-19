RNASQLite
RNASQLite is a tool for managing RNA-Seq data with SQLite. This package allows you to process RNA-Seq counts files, insert count files into a database, and retrieve sample information from the database.

Installation
First, navigate to the directory containing setup.py and install the package.

pip install .

Usage
Create Database
Create a new database. If a database file with the same name already exists, it will be deleted.

RNASQLite -create

Process and Split RNAseq Counts File
Process the given RNAseq counts file and save the count files for each sample in the counts directory. This step uses the gene info file (gene_info.csv) to add gene information.

RNASQLite -split path/to/your/rna_seq_counts_file.csv

Insert Count Files into Database
Read the count files from the counts directory and insert them into the database.

RNASQLite -load

Fetch All Samples from Database
Retrieve all sample information from the database.

RNASQLite -fetch



Description
RNASQLite/cli.py: Handles the command line interface.
RNASQLite/db_utils.py: Contains utility functions related to the database.
RNASQLite/process_file.py: Processes the given gene_info.csv and RNAseq counts file to generate count files.
gene_info.csv: CSV file containing gene information.
setup.py: Contains package metadata and dependencies.
README.md: This file, which includes the description and usage of the RNASQLite package.
