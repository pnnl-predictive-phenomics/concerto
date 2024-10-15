#!/bin/sh

###########README: lines starting with single '#' run. Lines starting with more than single '#' are treated as comments.

#https://confluence.pnnl.gov/confluence/display/RCWIKI/Schedule+Jobs
# (accessed on 3/6/2024 for deception partitions)

# -p means 'partition'
# Different partitions have different resources, limits and priorities depending on current users.
# Do not use ‘slurm’ partition since it consumes 64 cores!
# ref.https://confluence.pnnl.gov/confluence/pages/viewpage.action?spaceKey=RCWIKI&title=Deception

#SBATCH -p a100

##SBATCH -p a100,h100
#works

#h100_shared resulted in
#"torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 26.00 MiB. GPU"

##SBATCH -p dl
#RuntimeError: cutlassF: no kernel found to launch!

##SBATCH -p dlt
#torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate 26.00 MiB. GPU

##SBATCH -p fat
#RuntimeError: cutlassF: no kernel found to launch!

##SBATCH -p tonga
#RuntimeError: cutlassF: no kernel found to launch!

### The number after gpu: indicates how many GPUs you want to allocate for your job.
# SBATCH --gres=gpu:1    # requests 1 gpu
##SBATCH --gres=gpu:2    # requests 2 gpus (not 2nd gpu)

#Doonam confirmed that using 1 gpu and 8 gpu do not make any wallclock running time difference
#with chai-1 9/27/2024

#SBATCH -A peptide_design

#SBATCH -t 0-6:0:0  # Time limit in the format days-hours:minutes:seconds
##https://confluence.pnnl.gov/confluence/display/RC/Creating+a+Job+Script

#SBATCH -J output_11
#SBATCH --error  output_11_%j.err
#SBATCH --output output_11_%j.out

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
python /rcfs/projects/peptide_design/DN/model/chai-1/after_design/input_receptor_sequences_have_2_chain_ids/input_folder_for_chai_1/folder_of_py_files/output_11/output_11.py

end_time=$(date +%s)
 
elapsed_time=$((end_time - start_time))
 
hours=$((elapsed_time / 3600))
minutes=$(( (elapsed_time % 3600) / 60))
seconds=$((elapsed_time % 60))
 
echo "completed in ${hours}h:${minutes}m:${seconds}s."
