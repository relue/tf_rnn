import pandas as pd
import numpy as np
from numpy import pi, arange, sin, linspace
from bokeh.charts import Bar, output_file, show
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.autompg import autompg as df
from bokeh.models import LinearAxis, Range1d
from bokeh.models import Legend
from bokeh.io import output_file, show, vplot
from datetime import datetime as dt
from bokeh.models import DatetimeTickFormatter

#df = pd.read_csv('all.csv')
#pd.set_option('display.max_rows', 1000)

def convert_temp(source_temp=None):
   return (source_temp - 32.0) * (5.0/9.0)

def initDataFrame():
    df = pd.read_csv('energy_load/Load_history.csv', thousands=',', dtype='float', na_values=[''])
    dfT = pd.read_csv('energy_load/temperature_history.csv', thousands=',', dtype='float', na_values=[''],sep=';')

    for i in range(1, 25):
        dfT['c'+str(i)] = dfT['h'+str(i)].apply(convert_temp)

    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    dfT['date'] = pd.to_datetime(dfT[['year', 'month', 'day']])

    df['dayLoad'] = df['h1']
    for i in range(2, 25):
        df['dayLoad'] = df['dayLoad'] + df['h'+str(i)]

    dfT['dayTemp'] = dfT['c1']
    for i in range(2, 25):
        dfT['dayTemp'] = dfT['dayTemp'] + dfT['c'+str(i)]

    hourList = []
    for i in range(1,25):
        hourList.append('h'+str(i))

    hourList2 = []
    for i in range(1,25):
        hourList2.append('c'+str(i))

    dfNew = pd.melt(df, id_vars=['zone_id', 'year', 'month', 'day', 'dayLoad', 'date'], value_vars=hourList, var_name='hour', value_name='hourLoad')
    dfNewT = pd.melt(dfT, id_vars=['station_id', 'year', 'month', 'day', 'dayTemp', 'date'], value_vars=hourList2, var_name='hour', value_name='hourTemp')
    dfNew['hour'] = dfNew['hour'].apply(lambda x: x[1:])
    dfNewT['hour'] = dfNewT['hour'].apply(lambda x: x[1:])
    dfNewTP = dfNewT.pivot_table(values='hourTemp', index=['year', 'month', 'day', 'date', 'hour'], columns="station_id").reset_index(['year', 'month', 'day', 'date', 'hour'])
    dfNewM = pd.merge(dfNew, dfNewTP, on=['date','hour'])
    #dfNew.to_csv("allN.csv")
    return dfNew


df = initDataFrame()
#pd.melt(df, id_vars=['A'], value_vars=['B', 'C'], var_name='myVarname', value_name='myValname')

