try:
    import pretty_errors
except ImportError:
    exit("Run pip install pretty-errors")

import numpy as np
import pandas as pd
import glob
import os
import shutil
import sys
import argparse
import time  # Import time module for timing

def arrange_output():
    err_files = glob.glob("*.err")
    out_files = glob.glob("*.out")
    sbatch_files = glob.glob("*.sbatch")

    # Create 'err' and 'out' folders if they have files
    if err_files and not os.path.exists("err"):
        os.makedirs("err")
    if out_files and not os.path.exists("out"):
        os.makedirs("out")

    # Move '.err' and '.out' files into their respective folders
    for err_file in err_files:
        shutil.move(err_file, "err")
    for out_file in out_files:
        shutil.move(out_file, "out")

    # Move sbatch files into '../input/folder_of_sbatch_files'
    if sbatch_files:
        sbatch_destination = "../input/folder_of_sbatch_files"
        if not os.path.exists(sbatch_destination):
            os.makedirs(sbatch_destination)
        for sbatch_file in sbatch_files:
            shutil.move(sbatch_file, sbatch_destination)

    source = '../folder_of_py_files'
    destination = '../input/folder_of_py_files'

    # Move the 'folder_of_py_files' folder
    try:
        shutil.move(source, destination)
        print(f"Moved '{source}' to '{destination}'")
    except FileNotFoundError:
        print(f"The source '{source}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Rename 'folder_of_sbatch_files' to 'output'
    os.chdir("..")
    os.rename("folder_sbatch_files", "output")

    # Now, move 'err' and 'out' folders inside 'output' into 'output/log'
    os.chdir("output")
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if os.path.exists("err"):
        shutil.move("err", log_dir)
    if os.path.exists("out"):
        shutil.move("out", log_dir)
    os.chdir("..")

    # Define the path pattern
    base_directory = "output"
    output_subfolder = "output"

    # Recursively search for 'scores.model_idx_*.npz' files in the output/*/output directories
    for root, dirs, files in os.walk(base_directory):
        # Check if 'output_subfolder' is in the current path
        if output_subfolder in root:
            for file in files:
                if file.startswith("."):
                    continue  # Skip hidden files
                if file.startswith("scores.model_idx_") and file.endswith(".npz"):
                    file_path = os.path.join(root, file)
                    try:
                        # Load the npz file
                        data = np.load(file_path, allow_pickle=True)

                        # Iterate through the keys and save each array to a CSV file
                        for key in data.files:
                            if key not in ["ptm", "iptm"]:
                                continue

                            array_data = data[key]
                            df = pd.DataFrame(array_data)

                            csv_filename = file_path[:-4] + f".{key}.csv"
                            df.to_csv(csv_filename, index=False)
                    except Exception as e:
                        print(f"Failed to load file '{file_path}': {e}")
                        continue  # Skip this file and continue with others
###### end of def arrange_output()

def arrange_output_relocate_failed_and_succeeded_runs(N):
    print("Relocating failed and succeeded runs")
    os.chdir("output")

    folder_failed_run = "failed_run"
    folder_succeeded_run = "succeeded_run"

    if not os.path.exists(folder_failed_run):
        os.makedirs(folder_failed_run)
    if not os.path.exists(folder_succeeded_run):
        os.makedirs(folder_succeeded_run)

    excluded_folders = {
        "err", "out", folder_failed_run, folder_succeeded_run, "log",
        f"top_{N}_ptm_iptm", f"top_{N}_ptm_iptm_0_cif"
    }

    for each_dock_folder in os.listdir():
        if each_dock_folder.startswith("."):
            continue  # Skip hidden files and directories
        if each_dock_folder in excluded_folders:
            continue  # Skip the iteration for excluded folders
        if os.path.isdir(each_dock_folder):
            if not os.path.exists(os.path.join(each_dock_folder, "output")):
                # Move to failed_run
                shutil.move(each_dock_folder, os.path.join(folder_failed_run, each_dock_folder))
            else:
                # Move to succeeded_run
                shutil.move(each_dock_folder, os.path.join(folder_succeeded_run, each_dock_folder))
    os.chdir("..")
### end of def arrange_output_relocate_failed_and_succeeded_runs(N)

def arrange_output_save_csv_for_ptm_iptm(N):
    print(f"cwd:{os.getcwd()}")
    print("arrange_output_save_csv_for_ptm_iptm")

    df_iptm_ptm = pd.DataFrame(columns=['each_dock_folder', 'ptm', 'iptm'])

    come_back_to_here = os.getcwd()  # Save the current directory to come back later
    print(come_back_to_here)  # Should print the current directory

    os.chdir("output")

    # The succeeded runs are now in 'succeeded_run' folder
    os.chdir("succeeded_run")

    for each_dock_folder in os.listdir():
        if each_dock_folder.startswith("."):
            continue  # Skip hidden files and directories
        if not os.path.isdir(each_dock_folder):
            continue  # Skip if not a directory
        os.chdir(each_dock_folder)

        # Initialize dictionary to hold the data
        row_data = {'each_dock_folder': each_dock_folder}

        # Process PTM file
        ptm_file = os.path.join("output", "scores.model_idx_0.ptm.csv")
        if os.path.exists(ptm_file):
            df_ptm = pd.read_csv(ptm_file)
            if not df_ptm.empty:
                row_data['ptm'] = df_ptm.iloc[0, 0]
            else:
                row_data['ptm'] = np.nan
        else:
            row_data['ptm'] = np.nan

        # Process IPTM file
        iptm_file = os.path.join("output", "scores.model_idx_0.iptm.csv")
        if os.path.exists(iptm_file):
            df_iptm = pd.read_csv(iptm_file)
            if not df_iptm.empty:
                row_data['iptm'] = df_iptm.iloc[0, 0]
            else:
                row_data['iptm'] = np.nan
        else:
            row_data['iptm'] = np.nan

        # Only add the row if ptm and iptm are not NaN
        if not pd.isna(row_data['ptm']) and not pd.isna(row_data['iptm']):
            df_iptm_ptm = pd.concat([df_iptm_ptm, pd.DataFrame([row_data])], ignore_index=True)
        os.chdir("..")

    os.chdir(come_back_to_here)

    df_iptm_ptm['ptm+iptm'] = df_iptm_ptm['ptm'] + df_iptm_ptm['iptm']
    sorted_df_iptm_ptm = df_iptm_ptm.sort_values(by='ptm+iptm', ascending=False)

    # Save the CSV file into output folder with new name
    output_csv_path = os.path.join('output', 'df_sorted_by_sum_of_iptm_ptm.csv')
    sorted_df_iptm_ptm.to_csv(output_csv_path, index=False)

    # Create top_N_ptm_iptm folder inside output
    top_folder_name = os.path.join('output', f"top_{N}_ptm_iptm")
    if not os.path.exists(top_folder_name):
        os.makedirs(top_folder_name)

    top_dock_folders = sorted_df_iptm_ptm['each_dock_folder'].head(N)
    for each_dock_folder in top_dock_folders:
        src = os.path.join("output", "succeeded_run", each_dock_folder)
        dst = os.path.join(top_folder_name, each_dock_folder)
        shutil.copytree(src, dst)
### end of def arrange_output_save_csv_for_ptm_iptm(N)

def arrange_output_rename_top_N_ptm_iptm(N):
    come_back_to_here = os.getcwd()
    print(f"cwd:{come_back_to_here}")

    print("arrange_output_rename_top_N_ptm_iptm")

    top_folder_name = os.path.join('output', f"top_{N}_ptm_iptm")
    top_cif_folder_name = os.path.join('output', f"top_{N}_ptm_iptm_0_cif")

    if not os.path.exists(top_cif_folder_name):
        os.makedirs(top_cif_folder_name)

    # Change into the top_N_ptm_iptm directory
    os.chdir(top_folder_name)

    for each_dock_folder in os.listdir():
        if each_dock_folder.startswith("."):
            continue  # Skip hidden files and directories
        if not os.path.isdir(each_dock_folder):
            continue  # Skip if not a directory

        source = os.path.join(each_dock_folder, "output", "pred.model_idx_0.cif")
        destination = os.path.join(each_dock_folder, f"{each_dock_folder}_pred.model_idx_0.cif")

        if os.path.exists(source):
            print(f"source:{source} \ndestination:{destination}")
            shutil.move(source, destination)

            source = destination
            destination = os.path.join("..", os.path.basename(top_cif_folder_name), f"{each_dock_folder}_pred.model_idx_0.cif")
            print(f"\nFrom source:{source} \n to destination:{destination}")
            shutil.copy(source, destination)
        else:
            print(f"File not found: {source}")
            continue

    # Change back to the original directory
    os.chdir(come_back_to_here)

    # Now, rename files in the top_cif_folder
    os.chdir(top_cif_folder_name)
    for each_file in os.listdir():
        if each_file.startswith("."):
            continue  # Skip hidden files
        new_name = each_file.replace("_Gb2_Conformer3D_COMPOUND_CID_6424189_pred.model_idx_0", "")
        new_name = new_name.replace("all_sequences_after_", "")
        new_name = new_name.replace("RFDiffusion_AA_model_1_all_", "RFDiffusion_AA_model_1_LigandMPNN_")
        os.rename(each_file, new_name)
    # Change back to original directory
    os.chdir(come_back_to_here)
### end of def arrange_output_rename_top_N_ptm_iptm(N)


if __name__ == "__main__":
    if not hasattr(sys, "version_info") or sys.version_info < (3, 7):
        raise ValueError("Script requires Python 3.7 or higher!")

    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Arrange output files and select top N ptm_iptm entries.")
    parser.add_argument("--N", type=int, required=True, help="Number of top ptm_iptm entries (e.g., 30, 50) to process.")
    args = parser.parse_args()

    N = args.N  # Number of top entries to process

    cwd = os.getcwd()
    basefolder = os.path.basename(cwd)
    if basefolder != "folder_of_sbatch_files":
        print("This script should be run from the folder_sbatch_files folder")
        print(f"current folder is {cwd}")
        exit()

    # Measure the total time for the functions
    start_time = time.perf_counter()  # Start timing

    arrange_output()
    arrange_output_relocate_failed_and_succeeded_runs(N)
    arrange_output_save_csv_for_ptm_iptm(N)
    arrange_output_rename_top_N_ptm_iptm(N)

    end_time = time.perf_counter()  # End timing
    total_duration = end_time - start_time
    print(f"The total execution time was {total_duration:.1f} seconds")
