import pandas as pd
from typing import Union, List
from pathlib import Path


#function that inputs carbon source .csv file and returns list of metabolite names (without EX_ and _e)
def parse_carbsource_growth(fname: Union[str, Path]) -> List[str]:
    """
    Parse the carbon source growth names from a given .csv file.

    Args:
        fname (Union[str, Path]): A string or Path object representing the file path. The data is expected to have 'growth' and 'exchange' columns.

    Returns:
        List[str]: A list of strings containing the parsed carbon source growth names.
    """
    
    metab_growth_names = []
    
    # load data from file into a useable dataframe (pandas)
    df = pd.read_csv(fname)
    
    # go through each row, if the 'growth' column is true, remove the 'EX_' prefix and '_e' suffix of the string. 
    for _, row in df.iterrows():
        if row['growth']:  # Assuming there is a column named 'growth' with boolean values
            metab_name = row['exchange']
            # Remove 'EX_' prefix if it exists
            if metab_name.startswith('EX_'):
                metab_name = metab_name[3:] 
            # Remove '_e' suffix if it exists
            if metab_name.endswith('_e'):
                metab_name = metab_name[:-2]
            metab_growth_names.append(metab_name)
    return metab_growth_names