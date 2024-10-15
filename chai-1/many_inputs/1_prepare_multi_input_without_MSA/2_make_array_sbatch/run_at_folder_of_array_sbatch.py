import os
import glob

def generate_sbatch_script(max_concurrent_jobs=50):
    current_working_directory = os.getcwd()

    # Construct the path to 'folder_new_predict_structure_py' relative to the script directory
    target_dir = os.path.abspath(os.path.join(current_working_directory, '../folder_new_predict_structure_py'))
    
    # Use glob to find all matching scripts in the target directory
    #pattern = os.path.join(target_dir, 'omegaFold_not_ran_13052_simplified_header_*_each_predict_structure.py')
    pattern = os.path.join(target_dir, '*.py')
    
    script_paths = glob.glob(pattern)
    
    total_jobs = len(script_paths)
    if total_jobs == 0:
        print("No scripts found matching the pattern.")
        return

    if total_jobs > 1000:
        print("1k Total jobs worked well, but 2k total jobs failed with sbatch: error:\
               Batch job submission failed: Invalid job array specification")
        exit(1)
        
    script_paths_file = 'script_paths.txt'
    with open(script_paths_file, 'w') as f:
        for script_path in script_paths:
            f.write(script_path + '\n')
    print(f"Script paths have been written to '{script_paths_file}'.")
    
    sbatch_script = f"""#!/bin/bash

###SBATCH -p a100_shared
#failed with CUDA memory again 9/27/2024

#SBATCH -p a100
#SBATCH -A ppi_concerto
##SBATCH -t 0-6:0:0  # Time limit in the format days-hours:minutes:seconds
#SBATCH -t 4-0:0:0  # Time limit in the format days-hours:minutes:seconds
#SBATCH -J omegaFold_array_job
#SBATCH --error=omegaFold_array_job_%A_%a.err
#SBATCH --output=omegaFold_array_job_%A_%a.out
#SBATCH --array=1-{total_jobs}%{max_concurrent_jobs}

# Load necessary modules or activate your conda environment here
# For example:
# module load cuda/11.3
# source activate your_conda_environment_name

echo "Running on $(hostname)"
echo "SLURM_ARRAY_JOB_ID: $SLURM_ARRAY_JOB_ID"
echo "SLURM_ARRAY_TASK_ID: $SLURM_ARRAY_TASK_ID"

nvcc --version
nvidia-smi

start_time=$(date +%s)

# Read the script path corresponding to the task ID
script_path=$(sed -n "${{SLURM_ARRAY_TASK_ID}}p" {script_paths_file})

echo "Running script: $script_path"

# Run the script
python $script_path --task_id $SLURM_ARRAY_TASK_ID

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(( (elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

echo "Task $SLURM_ARRAY_TASK_ID completed in ${{hours}}h:${{minutes}}m:${{seconds}}s."
"""
    
    arrayed_sbatch = "use_sbatch_to_submit_this_array.sbatch"
    # Write the SBATCH script to a file
    with open(arrayed_sbatch, 'w') as f:
        f.write(sbatch_script)
    print(f"SBATCH script '{arrayed_sbatch}' has been generated.")
    
    # Change the permissions to make the script executable
    os.chmod(arrayed_sbatch, 0o777)
    print(f"Permissions for '{arrayed_sbatch}' have been set to rwxrwxrwx (777).")

if __name__ == "__main__":
    generate_sbatch_script()
