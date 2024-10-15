#!/bin/sh

###########README: lines starting with single '#' run. Lines starting with more than single '#' are treated as comments.

#https://confluence.pnnl.gov/confluence/display/RCWIKI/Schedule+Jobs
# (accessed on 3/6/2024 for deception partitions)

# -p means 'partition'
# Different partitions have different resources, limits and priorities depending on current users.
# Do not use ‘slurm’ partition since it consumes 64 cores!
# ref.https://confluence.pnnl.gov/confluence/pages/viewpage.action?spaceKey=RCWIKI&title=Deception


#SBATCH -p h100_shared,a100_shared,a100_80_shared
#h100 has 80GB gpu memory
#a100 has 40GB gpu memory

#Each Nvidia A100 machine has 8 GPUs

# a100_shared partition can have more than one job running at a time on a single node.
# running up to 4 a100_shared jobs tend to run at the same time (5th job is pending)

# -> Surprisingly, Trevor data ran at a100_shared and not fat_shared

##SBATCH -p tonga
##SBATCH -p dlt_shared

####SBATCH -p fat_shared
#"Nodes with 384GB of memory"
# -> Surprisingly, Trevor data cannot run at fat_shared due to out of memory error.

### The number after gpu: indicates how many GPUs you want to allocate for your job.
# SBATCH --gres=gpu:1    # requests 1 gpu
##SBATCH --gres=gpu:2    # requests 2 gpus (not 2nd gpu)

#SBATCH -A protein_design

#SBATCH -t 4-0 # for a100_shared
##SBATCH -t 7-0
##SBATCH -t 14:30:0
##https://confluence.pnnl.gov/confluence/display/RC/Creating+a+Job+Script

#SBATCH -J RFDiffusion_AA_model_9_all_sequences_after_LigandMPNN_9_Gb2_Conformer3D_COMPOUND_CID_6424189
#SBATCH --error  RFDiffusion_AA_model_9_all_sequences_after_LigandMPNN_9_Gb2_Conformer3D_COMPOUND_CID_6424189_%j.err
#SBATCH --output RFDiffusion_AA_model_9_all_sequences_after_LigandMPNN_9_Gb2_Conformer3D_COMPOUND_CID_6424189_%j.out

##SBATCH --mail-user=doonam.kim@pnnl.gov
##SBATCH --mail-type END
## slurm-*.out will be generated

## Local conda environment should be established before running this script
## For example, 
## source ~/.bash_profile_deception_personal_miniconda3.9_IsoNet_gpu_tf
## needs to be ran before sbatch

echo `nvcc --version`
nvidia-smi # nvidia-smi works only by sbatch. It does not work by login node.

#python examples/predict_structure.py 2>&1 | tee ps.log
python ../folder_new_predict_structure_py/RFDiffusion_AA_model_9_all_sequences_after_LigandMPNN_9_Gb2_Conformer3D_COMPOUND_CID_6424189_predict_structure.py
