Use >= python 3.7

(At deception) do
source /people/kimd999/.bash_profile_deception_personal_miniconda3.12.4_chai_lab

Refer working example folder's input and output folders as examples.

The 1st step (generate many py and sbatch files per each fasta sequence): (local concerto github repo)/chai-1/many_inputs/1_prepare_multi_input_without_MSA/1_make_non_array_sbatch/only_seq_exist/seq_at_fasta/all_input_seqs_are_ready_in_input_fasta_file/1_prepare_multi_inputs.py

The 2nd step (rewrite these many input files into an array): (local concerto github repo)/chai-1/many_inputs/1_prepare_multi_input_without_MSA/2_make_array_sbatch/run_at_folder_of_array_sbatch.py

The 3rd step (submit sbatch files): (local concerto github repo)/chai-1/many_inputs/2_submit_all_sbatch_files/2_submit_all_sbatch_files.py

The 4th step (arrange output results): (local concerto github repo)/chai-1/many_inputs/3_arrange_output
