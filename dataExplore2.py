from tkinter import *
from pandastable import Table, TableModel
import random
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import energyload_class
from time import *

#df = pd.read_pickle('rnnInput.pd')

class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, dataFrame, parent=None, ):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)

        self.table = pt = Table(f, dataframe=dataFrame,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

def showDF(df, breakIt = False):
    app = TestApp(df)
    #launch the app
    app.mainloop()
    if breakIt:
        exit()

import sys
pickle = sys.argv[1]
df = pd.read_pickle(pickle)
showDF(df)
