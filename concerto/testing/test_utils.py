from concerto.utils import parse_carbsource_growth, create_carveme_mediadb_df
import pandas as pd
import os

def test_parse_carbsource_growth():
    "Test the parse_carbsource_growth function."
    
    fname = os.path.join("concerto", "testing", "data", "biolog_carbon_curtobacterium1.csv")
    expected = ["dextrin", "pectin", "acgal", "abt__D", "arbt", "madg", 
                "pala", "raffin", "salcn", "stys","xylt", "gam", "Dara14lac" ] 
    actual = parse_carbsource_growth(fname)
    assert expected == actual


def test_create_carveme_mediadb_file():
    "Test the create_carveme_mediadb_df function."

    expected_results_fname = os.path.join("concerto", "testing", "data", "CarveMeMinimalMediaFile.csv")
    expected = pd.read_csv(expected_results_fname)
    actual = create_carveme_mediadb_df()
    pd.testing.assert_frame_equal(expected, actual)
    