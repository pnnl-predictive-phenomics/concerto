from pathlib import Path

import numpy as np
import torch

from chai_lab.chai1 import run_inference

# We use fasta-like format for inputs.
# Every record may encode protein, ligand, RNA or DNA
#  see example below

input_fasta = """
>protein|replace_this_w_receptor_name_base
replace_this_w_receptor_fasta_sequence
""".strip()

#fasta_path = Path("/tmp/example.fasta")
fasta_path = Path("replace_this_input_fasta_location")

# Get the directory part of the path (without the file)
fasta_dir = fasta_path.parent

# Create the directory if it doesn't exist (including any parent directories)
fasta_dir.mkdir(parents=True, exist_ok=True)



fasta_path.write_text(input_fasta)

#output_dir = Path("/tmp/outputs")
output_dir = Path("replace_this_output_location")
output_pdb_paths = run_inference(
    fasta_file=fasta_path,
    output_dir=output_dir,
    # 'default' setup
    num_trunk_recycles=3,
    num_diffn_timesteps=200,
    seed=42,
    device=torch.device("cuda:0"),
    use_esm_embeddings=True,
)

# Load pTM, ipTM, pLDDTs and clash scores for sample 2
scores = np.load(output_dir.joinpath("scores.model_idx_2.npz"))
