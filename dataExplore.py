from tkinter import *
from pandastable import Table, TableModel
import tensorflow as tf
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import energyload_class
from time import *

df = energyload_class.init_dfs(False, False)

class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('600x400+200+100')
        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)

        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

app = TestApp()
#launch the app
app.mainloop()
