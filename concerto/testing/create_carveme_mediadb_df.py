import pandas as pd 
def generate_mediadb(fname) : 
    """
    Returns: 
        df : a dataframe of combined metabolites and
        carbon sources, per minimal media source
    """
    #load carbonless minimal media file
    dfcmin = pd.read_csv(N-less_media.csv)

    #load biolog growth csv file
    dfbg = pd.read_csv(biolog_carbon_curtobacterium1.csv)

    #import biolog carbon file, assuming from utils.py?
    metab_growth_names = metab_growth_names

    #create a pandas dataframe of carbonless minimal media in carveme format
    c_min_med_dat = []

    for j in range(len(dfcmin["exchange"])): #We iterate through each reaction 
        #per carbon source metabolite from the carbonless minimal media file.
        #Here we just extract the metabolite part from the BiGG reaction ID. 
        #example: EX_csc_e --> csc
        carb_name = re.sub("EX_", "", ["exchange"][j])
        carb_name = re.sub("_e", "", carb_name)
        # We iterate through each of the compounds found on the biolog file.
        for i in range(len(dfbg["exchange"])):
            #Here we add create a new row with the information found on the previous dataframes.
            new_row = {
                "medium": "MM_[" + carb_name + "]", #Here we create the name of the medium. Ex: MM_[R_actn]
                "description": "Minimal medium (" + biolog_names["REAGENT"][j] + ")", #Here we specify a description of the minimal media.
                #NEED TO GET THESE TWO FROM SOMEWHERE--PM02 Bigg names??
                "compound": dfbg["compound"].iloc[i], #Here we add each of the compounds found on the minimal media of the model.
                "name": dfbg["name"].iloc[i] #Here we add each name of the compounds from the minimal media.
            }
            c_min_med_dat.append(new_row) # We append these new rows to the empty list. 
    return c_min_med_dat

#merge frames with extracted metab_growth_names?
allframes = [c_min_med_dat, metab_growth_names]

#create new dataframe from this merge?
mediadb_df = pd.concat(allframes)