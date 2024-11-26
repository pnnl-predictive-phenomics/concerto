#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# add in pathlib to make sure everyone can get this data

import pandas as pd
from cobra.io import read_sbml_model
from pathlib import Path

from micom import load_pickle


# set variables for importing data
HERE = Path(__file__).parent.resolve()
COM_MODEL = HERE.joinpath("Carbstor_Community/One.pickle")
NO_CURTO = HERE.joinpath("CarbStor_Community_NoCurtobacterium/One.pickle")


# load communities and define parameters
def main():
    com1 = load_pickle(COM_MODEL)
    result1 = com1.optimize(fluxes=True, pfba=True)
    print(result1.members)

    com2 = load_pickle(NO_CURTO)
    result2 = com2.optimize(fluxes=True, pfba=True)
    print(result2.members)


if __name__ == "__main__":
    main()
