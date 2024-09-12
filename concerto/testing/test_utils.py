from concerto.utils import parse_carbon_source_growth_file, parse_carbonless_media_file, create_carveme_mediadb_df
import pandas as pd
import os


def test_parse_carbon_source_growth_file():
    """Test the parse_carbon_source_growth_file function."""
    
    fname = os.path.join("concerto", "testing", "data", "biolog_carbon_curtobacterium1.csv")
    expected = ["dextrin", "pectin", "acgal", "abt__D", "arbt", "madg", 
                "pala", "raffin", "salcn", "stys","xylt", "gam", "Dara14lac" ] 
    actual = parse_carbon_source_growth_file(fname)
    assert expected == actual


def test_parse_carbonless_media_file():
    """Test the parse_carbonless_media_file function."""
    fname = os.path.join("concerto", "testing", "data", "csc009C-less_media.csv")
    expected_results_fname = os.path.join("concerto", "testing", "data", "expected_carbonless_media_df_from_csc009C_less_media.csv")
    actual_df = parse_carbonless_media_file(fname)
    expected_df = pd.read_csv(expected_results_fname)
    pd.testing.assert_frame_equal(expected_df, actual_df)


def test_create_carveme_mediadb_file():
    "Test the create_carveme_mediadb_df function."
    carbon_source_growth_file = os.path.join("concerto", "testing", "data", "biolog_carbon_curtobacterium1.csv")
    carbonless_media_file = os.path.join("concerto", "testing", "data", "csc009C-less_media.csv")
    expected_results_fname = os.path.join("concerto", "testing", "data", "expected_carveme_mediadb_from_biolog_curtobacterium1_and_csc009C_less_media.csv")
    expected_df = pd.read_csv(expected_results_fname)
    actual_df = create_carveme_mediadb_df(carbonless_media_file,carbon_source_growth_file)
    pd.testing.assert_frame_equal(expected_df, actual_df)