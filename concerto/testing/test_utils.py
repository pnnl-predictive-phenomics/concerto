from concerto.utils import parse_carbsource_growth

def test_parse_carbsource_growth():
    #we should expect an output of a list of metabolite names
    #check that expected names = actual names
    fname = "testing\\data\\biolog_carbon_curtobacterium1.csv"
    expected = ["dextrin", "pectin", "acgal", "abt__D", "arbt", "madg", 
                "pala", "raffin", "salcn", "stys","xylt", "gam", "Dara14lac" ] 
    actual = parse_carbsource_growth(fname)
    #check that the expected and actual are the same
    assert expected == actual