try:
  import pretty_errors
except:
   exit("Run pip install pretty-errors")

import glob, os, shutil, sys, time
from Bio import SeqIO
from pathlib import Path
from rdkit import Chem

def split_fasta_from_file(each_fasta_file):
    print(f"\n(split_fasta_from_file function) each_fasta_file: {each_fasta_file}")

    # Check if the file exists before trying to open it
    if not os.path.exists(each_fasta_file):
        print(f"Error: The specified file '{each_fasta_file}' does not exist.")
        return  # Exit the function if the file doesn't exist

    """Splits a fasta file into separate files for each sequence."""
    try:
        with open(each_fasta_file, 'r') as file:
            content = file.read().strip()
            sequences = content.split('>')  # Split based on FASTA header ('>')
            sequences = [seq for seq in sequences if seq]  # Filter out empty strings

            for idx, seq in enumerate(sequences, start=1):
                # Split sequence on the first newline to separate header from sequence
                parts = seq.split('\n', 1)  # Try to split into header and sequence
                
                if len(parts) == 2:
                    header = parts[0].strip()  # Get the header, ensure no extra spaces
                    sequence = parts[1].replace('\n', '').strip()  # Get sequence and remove newlines
                    
                    if sequence:  # Check if sequence is not empty
                        output_fa_each = each_fasta_file[:-6] + "_" + str(idx) + "_each.fa"  # Adjust extension handling
                        
                        with open(output_fa_each, 'w') as new_file:
                            new_file.write(f'>{header}\n{sequence}\n')
                    else:
                        print(f"Skipping empty sequence {idx} in file {each_fasta_file}.")
                else:
                    print(f"Skipping malformed entry {idx} in file {each_fasta_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")

###### end of def split_fasta_from_file(folder_of_fasta_files):


def prepare_one_input(each_fasta_file, template_path, account, partition):     
    each_fasta_file_base        = os.path.basename(each_fasta_file)
    each_fasta_file_base_no_ext = Path(each_fasta_file_base).stem
     
    template_predict_structure_py = os.path.join(template_path, "template_predict_structure.py")

    # Process each sequence in the fasta file
    for record in SeqIO.parse(each_fasta_file, "fasta"):
        receptor_fa_seq = str(record.seq)
        fasta_id = record.id  # This is 'EIKIBKLN_00017'

        new_predict_structure_py = fasta_id + ".py"

        with open(new_predict_structure_py, 'w') as f_out:
            with open(template_predict_structure_py, 'r') as f_in:
                for line in f_in:
                    new_line = line.replace("replace_this_w_receptor_name_base", fasta_id)
                    new_line = new_line.replace("replace_this_w_receptor_fasta_sequence", receptor_fa_seq)
                    new_line = new_line.replace("replace_this_input_fasta_location", \
                                                fasta_id + "/input.fasta")
                    new_line = new_line.replace("replace_this_output_location", \
                                                fasta_id + "/output")
                    f_out.write(new_line)
                    
        os.system(f"chmod +rwx {new_predict_structure_py}")

        # Move the new_predict_structure_py to 'folder_new_predict_structure_py'
        if not os.path.exists("folder_new_predict_structure_py"):
            os.makedirs("folder_new_predict_structure_py")

        destination = os.path.join("folder_new_predict_structure_py", new_predict_structure_py)

        # If the destination file already exists, remove it
        if os.path.exists(destination):
            os.remove(destination)

        shutil.move(new_predict_structure_py, destination)

        # Similarly, create the sbatch file for this fasta_id
        template_sbatch_path = os.path.join(template_path, "template_run_chai-1.sbatch")
         
        new_sbatch_file = fasta_id + ".sbatch"

        with open(new_sbatch_file, 'w') as f_out:
            with open(template_sbatch_path, 'r') as f_in:
                for line in f_in:
                    new_line = line.replace("replace_this_job", fasta_id)
                    new_line = new_line.replace("replace_this_partition", partition)
                    new_line = new_line.replace("replace_this_account", account)
                    new_line = new_line.replace("replace_this_predict_structure.py", \
                                                os.path.join("..","folder_new_predict_structure_py", \
                                                             new_predict_structure_py))
                    f_out.write(new_line)
                        
        os.system("chmod +rwx " + new_sbatch_file)

        if not os.path.exists("folder_sbatch_files"):
            os.makedirs("folder_sbatch_files")

        destination = os.path.join("folder_sbatch_files", new_sbatch_file)

        if os.path.exists(destination):
            os.remove(destination)

        shutil.move(new_sbatch_file, destination)

### end of def prepare_one_input(each_fasta_file, template_path, account, partition):


def prepare_many_inputs(folder_of_fasta_files, \
                        template_path, account, partition):
     
     folder_of_fasta_files = glob.glob(folder_of_fasta_files + "/*.fa") + glob.glob(folder_of_fasta_files + "/*.fasta")
     if len(folder_of_fasta_files) == 0:
          exit("No *.fa or *.fasta files in folder_of_fasta_files")

     for each_fasta_file in folder_of_fasta_files:
          prepare_one_input(each_fasta_file, template_path, account, partition)

     shutil.rmtree("all_each_sequence_folder")
##### end of def prepare_many_inputs(try_these_conditions, folder_of_input_tomofile):


def split_fasta_from_folder(folder_of_fasta_files):
     fasta_files = glob.glob(folder_of_fasta_files + "/*.fa") + glob.glob(folder_of_fasta_files + "/*.fasta")
     if len(fasta_files) == 0:
          exit("No *.fa or *.fasta files in folder_of_fasta_files")

     for each_fasta_file in fasta_files:
          #print (f"\n(split_fasta_from_folder function) each_fasta_file:{each_fasta_file}")
          split_fasta_from_file(each_fasta_file)
     
##### end of def split_fasta_from_folder(folder_of_fasta_files):


def prepare_all_each_sequence_folder(folder_of_input_fasta_files):
     if os.path.exists("all_each_sequence_folder"):
          shutil.rmtree("all_each_sequence_folder")

     os.system("mkdir all_each_sequence_folder")

     fasta_files = glob.glob(folder_of_input_fasta_files + "/*.fa") + glob.glob(folder_of_input_fasta_files + "/*.fasta")
     if len(fasta_files) == 0:
          exit("No *.fa or *.fasta files in folder_of_fasta_files")

     for each_fasta_file in fasta_files:
          # print (f"\n(prepare_all_each_sequence_folder function) current working directory:{os.getcwd()}")
          # print (f"\n(prepare_all_each_sequence_folder function) each_fasta_file:{each_fasta_file}")
          split_fasta_from_file(each_fasta_file)    
     # Construct the shell command using Python variables
     source_files = os.path.join(folder_of_input_fasta_files, "*_each.fa")
     destination_folder = "all_each_sequence_folder"

     # Use the constructed paths in the mv command
     move_command = f"mv {source_files} {destination_folder}"

     # Execute the shell command
     os.system(move_command)
##### end of def prepare_all_each_sequence_folder(folder_of_fasta_files):


if (__name__ == "__main__") :
     ########## <begin> basic checks
     if not hasattr(sys, "version_info") or sys.version_info < (3,7):
          raise ValueError("Script requires Python 3.7 or higher!")
     args = sys.argv[:]
     #print (len(args))
     if (len(args) < 3):
          #print (f"len(args):{len(args)}")
          print ("Specify                        <folder_of_fasta_files> <charging account> <partition>")
          print ("For example,\n")
          print ("python prepare_multi_inputs.py receptor                carbstor           a100")
          exit(1)
     ########## <end> basic checks
          
     starting_dir = os.getcwd()

     py_code = args[0]
     
     folder_of_input_fasta_files = os.path.abspath(args[1])
     if os.path.isdir(folder_of_input_fasta_files) == False:
          exit("folder_of_input_fasta_files should be a folder")
     
     account = str(args[2])
     partition = str(args[3])

     code_location = os.path.dirname(os.path.abspath(py_code))
     index_w_this_string = 'chai-1'
     index_of_path = code_location.index(index_w_this_string)
     template_path = os.path.join(code_location[:index_of_path], \
                                   os.path.join(index_w_this_string, "many_inputs", "1_prepare_multi_input_without_MSA", \
                                                "1_make_non_array_sbatch", \
                                                "only_seq_exist", "seq_at_fasta", \
                                                "all_input_seqs_are_ready_in_input_fasta_file", \
                                                "template"))

     start_time = time.time()
     
     prepare_all_each_sequence_folder(folder_of_input_fasta_files)
     
     prepare_many_inputs("all_each_sequence_folder", template_path, account, partition)
     end_time = time.time()
     # processing for 13k predictions took 6~29 minutes

     elapsed_time = end_time - start_time
     unit = "seconds" if elapsed_time < 60 else "minutes" if elapsed_time < 3600 else "hours"
     time_value = elapsed_time if unit == "seconds" else elapsed_time / 60 if unit == "minutes" else elapsed_time / 3600
     print(f"Preparing many inputs elapsed: {time_value:.1f} {unit}")
