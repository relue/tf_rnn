import cPickle as pickle
import pandas as pd
import numpy as np
#df = pickle.load("searchResults/sensi_manual3.pd")
df = pd.read_pickle("searchResults/sensi_manual3.pd")
df.to_csv('searchResults/sensi_manual3.csv')

df = pd.read_pickle("searchResults/rand_2.pd")
df.to_csv('searchResults/rand_2.csv')

df = pd.read_pickle("searchResults/tpe_4.pd")
df.to_csv('searchResults/tpe_4.csv')