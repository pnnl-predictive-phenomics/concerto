#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#add in pathlib to make sure everyone can get this data

import pandas as pd
from cobra.io import read_sbml_model
from pathlib import Path

from micom import Community
from micom.workflows import build, grow, tradeoff, fix_medium,build_database
from micom import load_pickle
from micom.viz import plot_tradeoff, plot_exchanges_per_sample, plot_growth


#set variables for importing data
HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
COM_MODEL = HERE.joinpath("One.pickle")
NO_CURTO = ROOT.joinpath("CarbStor_Community_NoCurtobacterium/One.pickle")

#load communities and define parameters
com1 = load_pickle(COM_MODEL)
result1 = com1.optimize(fluxes=True, pfba=True)
#result1
result1.summary()


# In[4]:

com2 = load_pickle(NO_CURTO)
result2 = com2.optimize(fluxes=True, pfba=True)
#result2
result2.summary()


# In[ ]:




