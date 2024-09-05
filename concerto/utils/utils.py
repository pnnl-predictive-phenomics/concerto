import pandas as pd
#function that inputs .csv files and returns list of metabolite names (without EX_ and _e)
def parse_carbsource_growth(fname):
    metab_growth_names = []
    #load data from file into a useable dataframe (pandas)
    pd.read_csv(fname)
    #go through each row, if growth column is true, string manipulation of exchange name
    
    return metab_growth_names