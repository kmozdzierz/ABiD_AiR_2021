# Metadata Guide

## Information about original dataset:

This analysis uses original data file, which is preserved in this documentation with the name '15_ZACHODNIOPOMORSKIE.csv'. 

Original dataset consist of 6 columns and 525 rows. Original columns' headers are polish language named. Columns of dataset give us informations about purchases of vacuume cleaners in one of the store chains. Informations were collected from locals of West Pomeranian Vovoideship in Poland.

We get data like: Days from purchase, Device's brand, Buyer's age, Buyer's gender and rating of product.


## Dataset Format

Header | Definition
---|------------
'Dni od zakupu' | `int` values between 10 and 16
'Marka' | 'Tefal', 'Electrolux', 'Beko', 'Samsung', 'Dyson'
'Wiek Kupujaceg' | `int` values between 18 and 76
'Płeć kupującego' | K, M or bd.
'Ocena' | `float` values between 0.0 and 5.0