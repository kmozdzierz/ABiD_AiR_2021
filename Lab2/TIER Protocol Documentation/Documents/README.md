## 1. Information about dataset

Analyzed dataset describe answers for seven question asked to some respondents about worriedness of potenial earthquake in the U.S. Moreover, we get informations about: gender, age, household earnings and U.S. Region of respondents.



## 2. The contents of the replication documentation:

All files need to replication are stored in following directories:

- Original dataset - ../Original Data/earthquake_data.csv
- Metadata info - ../Original Data/Metadata/MetadataGuide.md
- Command file (Jupyter Notebook) which generates output .csv file and graphs - ../Command Files/Lab2.ipynb
- Output file (.csv) and graphs (.png), after running Jupyter file, will be saved in - ../Analysis Data

## 3. Modifications of data

Included script written in Jupyter Notebook (.ipynb) anlyzes data in 3 steps:

1. Selects three proper columns of dataset. 
2. All NaN values are replaced with statement "No answer given"
3. Exports processed data in .csv file and saves graph presentation of processed data

## 4. Instructions for replicating the study

To run command files of this analisys on your own, you need to have installed following Python (ver. >= 3.7) libraries and additions:

* Jupyter Notebook
* Numpy
* Pandas
* Matplotlib

Then all you have to do is run the code included in Lab2.ipynb. 



