#!/bin/bash

#SBATCH -p a100_shared,a100_80_shared
#SBATCH -A ppi_concerto
#SBATCH -t 0-6:0:0  # Time limit in the format days-hours:minutes:seconds
#SBATCH -J omegaFold_array_job
#SBATCH --error=omegaFold_array_job_%A_%a.err
#SBATCH --output=omegaFold_array_job_%A_%a.out
#SBATCH --array=1-2%50

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
script_path=$(sed -n "${SLURM_ARRAY_TASK_ID}p" script_paths.txt)

echo "Running script: $script_path"

# Run the script
python $script_path --task_id $SLURM_ARRAY_TASK_ID

end_time=$(date +%s)

elapsed_time=$((end_time - start_time))

hours=$((elapsed_time / 3600))
minutes=$(( (elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))

echo "Task $SLURM_ARRAY_TASK_ID completed in ${hours}h:${minutes}m:${seconds}s."
