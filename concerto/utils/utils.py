import pandas as pd
import re
from typing import Union, List
from pathlib import Path

def parse_carbsource_growth(fname: Union[str, Path]) -> List[str]:
    """
    Parse the carbon source growth names from a given .csv file.

    Args:
        fname (Union[str, Path]): A string or Path object representing the file path. The data is expected 
        to have 'growth' and 'exchange' columns.

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
def parse_carbonless_min_media(carbless_min_media_file):
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
                              biolog_growth_file):
    """
    Creates carveme media dataframe by combining carbon source 
        + minimal media file with biolog growth file.
    Returns: 
        df : a dataframe of combined metabolites and
        carbon sources, per minimal media source
    """
    #import biolog carbon file, assuming from utils.py?
    carb_source_growth_names = parse_carbsource_growth(biolog_growth_file) #picks out where carbonsource growth 
    #= true
    #goes through each name in this list and iterates through to update media and description per 
    #carbsource name on that list
    
    #create a pandas dataframe of carbonless minimal media in carveme format
    carbonless_min_media_df = parse_carbonless_min_media(carbless_min_media_file)
    #1. iterate through each exchanged carbon source growth in biolog
    all_dataframes_for_concating = []
    all_dataframes_for_concating.append(carbonless_min_media_df)
#   2. for each name, make a copy of the carbonless_min_media dataframe with the same length
    num_rows = carbonless_min_media_df.shape[0]
    for carb_name in carb_source_growth_names:
        temp_carb_name_df = carbonless_min_media_df.copy(deep = True)
        #change media and description names to match carbon source
        temp_media_list = [f"BL[{carb_name}]"] * num_rows
        temp_description_list = [f"Biolog [{carb_name}] Media"] * num_rows
        temp_carb_name_df["media"] = temp_media_list
        temp_carb_name_df["description"] = temp_description_list
        #add new row for carbon source growth
        carb_source_data_dictionary = {
            "media" : f"BL[{carb_name}]", 
            "description" : f"Biolog [{carb_name}] Media",
            "compound" : carb_name,
            "name": carb_name,
        }
        print(carb_source_data_dictionary)
        
         #3. add a new row top temp dataframe for carbon to include in media of dictionary
        temp_carbon_source_df = pd.DataFrame(carb_source_data_dictionary)
        fin_carbon_source_df = pd.concat([temp_carbon_source_df, temp_carb_name_df], 
                                         ignore_index = True)
        # 4. append fin_carbon_source_df to all_dataframes_for_concating
        all_dataframes_for_concating.append(fin_carbon_source_df)
    return pd.concat(all_dataframes_for_concating, ignore_index= True)

#for testing: 
carveme_mediadb_df = create_carveme_mediadb_df("C:\\Users\\lint730\\concerto\\concerto\\testing\\data\\csc009C-less_media.csv",
                          "C:\\Users\\lint730\\concerto\\concerto\\testing\\data\\biolog_carbon_curtobacterium1.csv",
                          )
carveme_mediadb_df.to_csv("C:\\Users\\lint730\\concerto\\concerto\\testing\\data\\carveme_media_db.csv")