try:
  import pretty_errors
except:
   exit("Run pip install pretty-errors")

import numpy as np
import pandas as pd
import glob, os, shutil, sys

import os
import shutil

def copy_predictions():
    excluded_extensions = {".err", ".out", ".sbatch"}  # Define file extensions to exclude
    destination_folder = "../folder_pred_model_idx_0"
    
    # Ensure destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate over files and folders in the current directory
    for each_file_or_folder in os.listdir():
        if each_file_or_folder.endswith(tuple(excluded_extensions)) \
          or each_file_or_folder in {".DS_Store"}:
            continue  # Skip excluded files and folders

        if os.path.isdir(each_file_or_folder):
            print(f"Processing: {each_file_or_folder}")
            
            # Construct the path to the target file
            source_file = os.path.join(each_file_or_folder, "output", "pred.model_idx_0.cif")
            
            # Check if the source file exists
            if os.path.exists(source_file):
                # Define the renamed destination file
                destination_file = os.path.join(destination_folder, f"{each_file_or_folder}_pred.model_idx_0.cif")
                
                # Copy the file and rename it
                shutil.copy(source_file, destination_file)
                print(f"Copied and renamed {source_file} to {destination_file}")
            else:
                print(f"Source file {source_file} does not exist.")

### end of def copy_predictions():


if (__name__ == "__main__") :
  if not hasattr(sys, "version_info") or sys.version_info < (3,7):
    raise ValueError("Script requires Python 3.7 or higher!")

  cwd = os.getcwd()
  basefolder = os.path.basename(cwd)
  if basefolder != "folder_sbatch_files":
    print("This script should be run from the folder_sbatch_files folder")
    exit()

  copy_predictions()