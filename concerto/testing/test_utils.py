from concerto.utils import parse_carbsource_growth
import os

def test_parse_carbsource_growth():
    "Test the parse_carbsource_growth function."
    
    fname = os.path.join("concerto", "testing", "data", "biolog_carbon_curtobacterium1.csv")
    expected = ["dextrin", "pectin", "acgal", "abt__D", "arbt", "madg", 
                "pala", "raffin", "salcn", "stys","xylt", "gam", "Dara14lac" ] 
    actual = parse_carbsource_growth(fname)
    assert expected == actual