import pytest
import pandas as pd
import re
from pathlib import Path

from concerto.Metabolic_Data_Files.Metabolite_Data import (
    extract_BioCycIDs,
    Confirm_All_BioCycIDs,
    Confirm_BioCycIDs_n_Values,
)
from concerto.Metabolic_Data_Files.Metabolite_Data import (
    extract_BioCycIDs,
    Confirm_All_BioCycIDs,
    Confirm_BioCycIDs_n_Values,
)

HERE = Path(__file__).parent.resolve()
Generated_File = pd.read_csv(
   HERE.joinpath("../concerto/Metabolic_Data_files/BioCycID_Processed_Metabolomic_Data_NoRhodOutlier_6_14_24.tsv"
    ),
    delimiter="\t",
)

file_hilpos = HERE.joinpath("successful_hilpos.csv", "r").as_posix()
file_hilneg = HERE.joinpath("successful_hilneg.csv", "r").as_posix()
Transposed_File = HERE.joinpath(
    "Transposed_Processed_Metabolomics_Data_NoRhodOutlier_6_14_24.csv"
).as_posix()

def test_Confirm_All_BioCycIDs():
    Metabolite_n_ID_HILPos, Metabolite_n_ID_Ambiguous_HILPos = extract_BioCycIDs(file_hilpos, "_HILPos")
    Metabolite_n_ID_HILNeg, Metabolite_n_ID_Ambiguous_HILNeg = extract_BioCycIDs(file_hilneg, "_HILNeg")
    result_1 = Confirm_All_BioCycIDs(Generated_File, Metabolite_n_ID_HILPos, Metabolite_n_ID_Ambiguous_HILPos)
    result_2 = Confirm_All_BioCycIDs(Generated_File, Metabolite_n_ID_HILNeg, Metabolite_n_ID_Ambiguous_HILNeg)
    assert result_1 == True and result_2 == True

def test_Confirm_BioCycIDs_n_Values():
    result_3 = Confirm_BioCycIDs_n_Values(Generated_File, Transposed_File)
    assert result_3 == True

