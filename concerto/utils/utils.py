import pandas as pd
import re
from typing import Union, List
from pathlib import Path


def parse_carbon_source_growth_file(carbon_source_growth_file: Union[str, Path]) -> List[str]:
    """
    Parse the carbon source growth names from a given .csv file.

    Args:
        fname (Union[str, Path]): A string or Path object representing the file path. The data is expected 
        to have 'growth' (boolean) and 'exchange' (string) columns.

    Returns:
        List[str]: A list of strings containing the parsed carbon source growth names.
    """
    
    carbon_growth_names = []
    
    # load data from file into a useable dataframe (pandas)
    carbon_source_df = pd.read_csv(carbon_source_growth_file)
    
    # go through each row, if the 'growth' column is true, remove the 'EX_' prefix and '_e' suffix of the string. 
    for _, row in carbon_source_df.iterrows():
        if row['growth']:  # Assuming there is a column named 'growth' with boolean values
            carbon_source_name = row['exchange']
            # Remove 'EX_' prefix if it exists
            if carbon_source_name.startswith('EX_'):
                carbon_source_name = carbon_source_name[3:] 
            # Remove '_e' suffix if it exists
            if carbon_source_name.endswith('_e'):
                carbon_source_name = carbon_source_name[:-2]
            carbon_growth_names.append(carbon_source_name)
    return carbon_growth_names


def parse_carbonless_media_file(carbonless_media_file: Union[str, Path]) -> pd.DataFrame:
    """
    Parses a carbonless media file and extracts relevant information.

    Args:
        carbonless_media_file: A .csv file containing carbonless media data. Should contain an "exchange" column of metabolite names.

    Returns:
        pd.DataFrame: A DataFrame containing parsed data with columns for medium, description, compound, and name.
    """

    #load carbonless minimal media file, and create list of "medium" and "description" values
    carbonless_media_df = pd.read_csv(carbonless_media_file)
    num_rows = carbonless_media_df.shape[0]
    medium_list = ["MM"] * num_rows
    description_list = ["minimal media"] * num_rows

    # iterate through each metabolite, remove 'EX_' and '_e' from string, and
    # create a dataframe that includes the "medium", "description", "compound", and "name"
    compound_list = []
    name_list = []
    for _, row in carbonless_media_df.iterrows():
        met_name = re.sub("EX_", "", row["exchange"])
        met_name = re.sub("_e", "", met_name)
        compound_list.append(met_name)  # BIGG ID
        name_list.append(met_name) 
    data_dictionary = {
        "medium": medium_list, 
        "description": description_list,
        "compound": compound_list, 
        "name": name_list
    }
    return pd.DataFrame(data_dictionary)


def create_carveme_mediadb_df(carbonless_media_file: Union[str, Path], 
                              carbon_source_growth_file: Union[str, Path])->pd.DataFrame:
    """
    Creates a dataframe by combining a carbonless minimal media file with a biolog growth file to generate a CarveMe media database.

    Args:
        carbonless_media_file: A .csv file containing carbonless minimal media data.
        carbon_source_growth_file: A .csv file containing biolog growth data.

    Returns:
        pd.DataFrame: A dataframe of combined metabolites and carbon sources per minimal media source.
    """

    # get carbon source names, minimal media, and number of rows
    carbon_source_growth_names = parse_carbon_source_growth_file(carbon_source_growth_file) 
    carbonless_min_media_df = parse_carbonless_media_file(carbonless_media_file)
    media_dfs = []
    media_dfs.append(carbonless_min_media_df)
    num_rows = carbonless_min_media_df.shape[0]

    # iterate through each carbon source name, creating a new dataframe w/ carbon source
    for carbon_name in carbon_source_growth_names:
        _carbon_df = carbonless_min_media_df.copy(deep = True) # everything except carbon source

        # update the "medium" and "description" columns
        _media_list = [f"BL[{carbon_name}]"] * num_rows
        _description_list = [f"Biolog [{carbon_name}] Media"] * num_rows
        _carbon_df["medium"] = _media_list
        _carbon_df["description"] = _description_list

        # insert a new row for the carbon source, append to media dataframe list
        _carbon_source_data_dictionary = {
            "medium" : [f"BL[{carbon_name}]"], 
            "description" : [f"Biolog [{carbon_name}] Media"],
            "compound" : [carbon_name],
            "name": [carbon_name],
        }
        _carbon_source_df = pd.DataFrame(_carbon_source_data_dictionary)  # only carbon source
        media_dfs.append(pd.concat([_carbon_source_df, _carbon_df], 
                                         ignore_index = True))
    return pd.concat(media_dfs, ignore_index= True)