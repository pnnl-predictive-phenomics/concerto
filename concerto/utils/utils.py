import pandas as pd
import re
from typing import Union, List
from pathlib import Path
from cobra.core import Model


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

#transform carbonless media into dataframe
def parse_carbonless_min_media(carbless_min_media_file,
                               universal):
    #lists with name of data that corresponds
    compound_list = []
    name_list = []

    #load carbonless minimal media filec
    df_carbonless_min_media = pd.read_csv(carbless_min_media_file)
    num_rows = df_carbonless_min_media.shape[0]
    #other two lists with name of data that corresponds
    medium_list = ["MM"] * num_rows
    description_list = ["minimal media"] * num_rows

    for _, row in df_carbonless_min_media.iterrows():
         #We iterate through each reaction 
        #per carbon source metabolite from the carbonless minimal media file.
        #Here we just extract the metabolite part from the BiGG reaction ID. 
        #example: EX_csc_e --> csc
        carb_name = re.sub("EX_", "", row["exchange"])
        carb_name = re.sub("_e", "", carb_name)
        #carb_name = universal.reactions.get_by_id(row['exchange']).metabolites[0]
        #49: getting metabolite compound names from universal
        compound_list.append(carb_name)
        name_list.append(carb_name)
    data_dictionary = {
        #pattern: key then value
        #assign name for column and what's going to go in column
        "medium": medium_list, 
        "description": description_list,
        "compound": compound_list, 
        "name": name_list
    }
    return pd.DataFrame(data_dictionary)


def create_carveme_mediadb_df(carbless_min_media_file, 
                              biolog_growth_file,
                              universal):
    """
    Creates carveme media dataframe by combining carbon source 
        + minimal media file with biolog growth file.
    Returns: 
        df : a dataframe of combined metabolites and
        carbon sources, per minimal media source
    """
    #import biolog carbon file, assuming from utils.py?
    carb_source_growth_names = parse_carbsource_growth(biolog_growth_file)
    #   TO DO: create a new list and append to list
    
    #create a pandas dataframe of carbonless minimal media in carveme format
    carbonless_min_media_df = parse_carbonless_min_media(carbless_min_media_file)
#TO DO: 1. iterate through each exchanged carbon source growth in biolog
#   2. for each one, make a copy of the carbonless_min_media dataframe
#   3. rename 'media' and 'description' columns
#   4. append carbon source row if growth = TRUE
#   5. end:  add to list of dataframes, 
#       concat all dataframes together

        # We iterate through each of the compounds found on the biolog file.
        #for i in range(len(dfbg["exchange"])):
            #Here we add create a new row with the information found on the previous dataframes.
            #new_row = {
                #"medium": "MM_[" + carb_name + "]", #Here we create the name of the medium. Ex: MM_[R_actn]
                #"description": "Minimal medium (" + biolog_names["REAGENT"][j] + ")", #Here we specify a description of the minimal media.
                #NEED TO GET THESE TWO FROM SOMEWHERE--universal model
                #"compound": dfbg["compound"].iloc[i], #Here we add each of the compounds found on the minimal media of the model.
    #             "name": dfbg["name"].iloc[i] #Here we add each name of the compounds from the minimal media.
    #         }
    #         c_min_med_dat.append(new_row) # We append these new rows to the empty list. 
    # return c_min_med_dat

#merge frames with extracted metab_growth_names?
# allframes = [c_min_med_dat, metab_growth_names]

# #create new dataframe from this merge?
# mediadb_df = pd.concat(allframes)
    pass
