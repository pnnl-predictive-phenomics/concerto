try:
  import pretty_errors
except:
   exit("Run pip install pretty-errors")

import glob, os, sys

def submit_at_sbatch_folder():
  sbatch_files_in_current_folder = glob.glob("*.sbatch")

  for sbatch_file_name in sbatch_files_in_current_folder:
    cmd = "sbatch " + sbatch_file_name
    os.system(cmd)
###### end of def submit_at_sbatch_folder():

if (__name__ == "__main__") :
  if not hasattr(sys, "version_info") or sys.version_info < (3,7):
    raise ValueError("Script requires Python 3.7 or higher!")

  submit_at_sbatch_folder()
