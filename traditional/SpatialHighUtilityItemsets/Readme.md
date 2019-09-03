# Spatial High Utility Itemset Mining (SHUIM)

SHUIM aims to find all itemsets that have high utility and exist close to one another in a spatiotemporal database.

The command to execute the program is as follows:
<  python3 SpatialAlgoEFIM.py **data_file**  **neighborhood_file** **output_file** *min_Util*


The input format of the files is as follows:
1. data_file:   items:transaction utility:pmu values of items
2. neighborhood_file:       item, list of its neighbors
3. output_file:  pattern, utility
