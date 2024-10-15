#!/bin/sh

###########README: lines starting with single '#' run. Lines starting with more than single '#' are treated as comments.

#https://confluence.pnnl.gov/confluence/display/RCWIKI/Schedule+Jobs
# (accessed on 3/6/2024 for deception partitions)

# -p means 'partition'
# Different partitions have different resources, limits and priorities depending on current users.
# Do not use ‘slurm’ partition since it consumes 64 cores!
# ref.https://confluence.pnnl.gov/confluence/pages/viewpage.action?spaceKey=RCWIKI&title=Deception

#SBATCH -p h100,a100

### The number after gpu: indicates how many GPUs you want to allocate for your job.
# SBATCH --gres=gpu:1    # requests 1 gpu
##SBATCH --gres=gpu:2    # requests 2 gpus (not 2nd gpu)

#SBATCH -A nwbrave

#SBATCH -t 4-0 # for a100_shared
##SBATCH -t 7-0
##SBATCH -t 14:30:0
##https://confluence.pnnl.gov/confluence/display/RC/Creating+a+Job+Script

#SBATCH -J ADO99788.1
#SBATCH --error  ADO99788.1_%j.err
#SBATCH --output ADO99788.1_%j.out

##SBATCH --mail-user=doonam.kim@pnnl.gov
##SBATCH --mail-type END
## slurm-*.out will be generated

## Local conda environment should be established before running this script
## For example, 
## source ~/.bash_profile_deception_personal_miniconda3.9_IsoNet_gpu_tf
## needs to be ran before sbatch

echo `nvcc --version`
nvidia-smi # nvidia-smi works only by sbatch. It does not work by login node.

start_time=$(date +%s)

#python examples/predict_structure.py 2>&1 | tee ps.log
python ../folder_new_predict_structure_py/ADO99788.1_predict_structure.py

end_time=$(date +%s)
 
elapsed_time=$((end_time - start_time))
 
hours=$((elapsed_time / 3600))
minutes=$(( (elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))
 
echo "Completed in ${hours}h:${minutes}m:${seconds}s."
