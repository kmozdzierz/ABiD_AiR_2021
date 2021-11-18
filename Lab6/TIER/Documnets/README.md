# 1. Infotmation about dataset 

Analyzed dataset includes information about purchases of vacuume cleaners in one of the store chains. Informations were collected from locals of West Pomeranian Vovoideship in Poland.

We get information about: Days from purchase, Device's brand, Buyer's age, Buyer's gender and rating of product.

# 2. The contents of the replication documentation:

All files need to replication are stored in following directories:

- Original dataset - ../Original Data/15_ZACHODNIOPOMORSKIE.csv
- Metadata info - ../Original Data/Metadata/MetadataGuide.md
- Command file (Jupyter Notebook) which checks, cleans data and generates output .csv file - ../Command Files/lab6.ipynb
- Output file (.csv), after running Jupyter file, will be saved in - ../Analysis Data/West_pomeranian_data.csv

## 3. Modifications of data

There are two scripts written in Jupyter Notebook (.ipynb) which anlyzes data in few steps:

'lab6.ipynb' in Command Files:

1. Reads original .csv file and checks basic informations about dataset like columns names or data types.
2. Headers of original data are polish language named, so script changes it into english names.
3. Drops redundant column with rows numbering and replaces 'bd.' statements with None value.
3. Exports processed data in .csv file.

'DataAppendix.ipynb':

1. Analyzes data for visual presentation and statistical purposes.


## 4. Instructions for replicating the study

To run command files of this analisys on your own, you need to have installed following Python (ver. >= 3.7) libraries and additions:

* Jupyter Notebook
* Numpy
* Pandas
* Matplotlib

Then all you have to do is run the code included in lab6.ipynb and DataAppendix.ipynb. 

*Visual Studio Code is recommended for openning and analyzing project.
