#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from cobra.io import read_sbml_model

from micom import Community
from micom.workflows import build, grow, tradeoff, fix_medium,build_database
from micom import load_pickle
from micom.viz import plot_tradeoff, plot_exchanges_per_sample, plot_growth

com1 = load_pickle("/Users/rodr579/Library/CloudStorage/OneDrive-PNNL/venv/CarbStor_Community/One.pickle")
result1 = com1.optimize(fluxes=True, pfba=True)
#result1
result1.summary()


# In[4]:


com2 = load_pickle("/Users/rodr579/Library/CloudStorage/OneDrive-PNNL/venv/CarbStor_Community_NoCurtobacterium/One.pickle")
result2 = com2.optimize(fluxes=True, pfba=True)
#result2
result2.summary()


# In[ ]:




