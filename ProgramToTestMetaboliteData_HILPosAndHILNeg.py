import pandas as pd
import re
# Open the file that we generated previously.
Generated_File = pd.read_csv("BioCycID_Processed_Metabolomic_Data_NoRhodOutlier_6_14_24.tsv", delimiter="\t")
#Here we read the "Succesful" files.
file_hilpos = open("successful_hilpos.csv", "r")
file_hilneg = open("successful_hilneg.csv", "r")
#This function extracts the Metabolite Names and their corresponding BioCycIDs in the form of a dictionary
# from the "Succesful" files.
def extract_BioCycIDs(file, string):
    header = file.readline()
    columns = file.readline()
    Metabolite_n_ID = {} #A dictionary for metabolites with a single BioCycID.
    Metabolite_n_ID_Ambiguous = {} #A dictionary for metabolites with multiple BioCycIDs.
    for line in file: #We iterate through each line of each file.
        line = line.strip() #We eliminate the lines that appear to be blank.
        if line:
            line_parts = re.split("\t", line) # We separate each line by each tab.
            if len(line_parts) >= 5: #If after separating the line there are 5 elements or more (Succesful List):
                metabolite = line_parts[0] #Extract the 1st element.
                biocyc_id = line_parts[4]#And the 5th element too.
                Metabolite_n_ID[str(metabolite) + string] = str(biocyc_id) #Add it to the dictionary.
            elif len(line_parts) == 4: #If after separating the line there are 4 elements (Ambiguous List):
                metabolite = line_parts[0] #Extract first element.
                biocyc_id = re.split(",", line_parts[3]) # Extract 4rth element.
                Metabolite_n_ID_Ambiguous[str(metabolite) + string] = biocyc_id #Add it to the dictionary.
    return Metabolite_n_ID, Metabolite_n_ID_Ambiguous #Return the dictionaries.

#Apply the function to the "Succesful" files.
Metabolite_n_ID_HILPos, Metabolite_n_ID_Ambiguous_HILPos = extract_BioCycIDs(file_hilpos, "_HILPos")
Metabolite_n_ID_HILNeg, Metabolite_n_ID_Ambiguous_HILNeg = extract_BioCycIDs(file_hilneg, "_HILNeg")

#This function will confirm that all BioCycIDs correspond to their respective metabolite.
def Confirm_All_BioCycIDs(file, dictionary, ambiguous):
    Confirm_BioCycIDs = [] #We create an empty list.
    for key in dictionary: #We iterate through each key of the dictionary containing the metabolites with a single ID.
        for i in range(len(file["Metabolites"])): # We iterate through the number of elements in the "Metabolites" column.
            #We verify if the keys of the dictionary are equal to the elements found in the file we generated,
            # we also check if the values assign to the keys in the dictionary are the same as the elements found
            # in the "BioCycID" column of the file.
            if key == file["Metabolites"][i] and dictionary[key] == file["BioCycID"][i]:
                Confirm_BioCycIDs.append(True) #If the condition is met then we append a True value to the list.
    #Here we do the same as the previous code but adapted for the metabolites with multiple BioCycIDs. We
    for key in ambiguous:
        for i in range(len(file["Metabolites"])):
            if key == file["Metabolites"][i]:
                if file["BioCycID"][i] in ambiguous[key]:
                    Confirm_BioCycIDs.append(True)
    if all(Confirm_BioCycIDs): #If the list contains only True values the we have confirme that all BioCycIds are
        print("All BioCycIDs correspond to their rightful Metabolite.") # assigned to their correspongi metabolite.
        return True
    else:
        return False
        print("Something is wrong! Go back!")

#We apply the previous function to the File Generated and the dictionaries we created previously.
#Confirm_All_BioCycIDs(Generated_File, Metabolite_n_ID_HILPos, Metabolite_n_ID_Ambiguous_HILPos)
#Confirm_All_BioCycIDs(Generated_File, Metabolite_n_ID_HILNeg, Metabolite_n_ID_Ambiguous_HILNeg)

#We open the Transposed file we created previously.
Transposed_File = pd.read_csv("Transposed_Processed_Metabolomics_Data_NoRhodOutlier_6_14_24.csv")

def Confirm_BioCycIDs_n_Values(Generated_File, Transposed_File):
    # We extract the column names of the file.
    column_names = Generated_File.columns.tolist()
    # We remove the columns "BioCycID" and "Metabolites".
    column_names.pop(0)
    column_names.pop(0)

    Confirm_BioCycIDs_n_Info = [] #We create a list to store True values.
    for condition in column_names: #We iterate through each column we extracted previously.
        for i in range(len(Generated_File[condition])): #We iterate through the number of elements of each column in the Generated File.
            for j in range(len(Transposed_File[condition])): #We iterate through the number of elements of each column in the Transposed File.
                #If a metabolite name of the Generated File is the same as a metabolite name of the Transposed File:
                if Generated_File["Metabolites"][i] == Transposed_File["Metabolites"][j]:
                    #And if an element of the condition column in the Generated File is the same as an element of the condition column of the Transposed File.
                    if Generated_File[condition][i] == Transposed_File[condition][j]:
                        Confirm_BioCycIDs_n_Info.append(True) #Then add a True value to the list.
    #If all values in the list are True, then all number values are assigned accordingly to each metabolite.
    if all(Confirm_BioCycIDs_n_Info):
        print("All values are assigned to their respective metabolite accordingly.")
        return True
    else:
        print("Something is wrong! Go back!")
        return False
#Confirm_BioCycIDs_n_Values(Generated_File, Transposed_File)