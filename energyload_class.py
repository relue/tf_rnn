import pandas as pd
import numpy as np
from numpy import pi, arange, sin, linspace
from bokeh.charts import Bar, output_file, show
from bokeh.plotting import figure, show, output_file
from bokeh.sampledata.autompg import autompg as df
from bokeh.models import LinearAxis, Range1d
from bokeh.models import Legend
from bokeh.io import output_file, show, vplot, gridplot
from bokeh.models import DatetimeTickFormatter
from bokeh.models import PrintfTickFormatter
from bokeh.charts import HeatMap, output_file, show, TimeSeries
import itertools
import calendar
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Dropdown



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

    dfNew = pd.merge(df, dfT, on='date')
    dfNew.to_csv("all.csv")
    return dfNew

def initDataFrameHourly():
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

    dfNew = pd.melt(df, id_vars=['year', 'month', 'day',  'date', 'dayLoad', 'zone_id'], value_vars=hourList, var_name='hour', value_name='hourLoad')
    dfNewT = pd.melt(dfT, id_vars=['station_id', 'year', 'month', 'day', 'dayTemp', 'date'], value_vars=hourList2, var_name='hour', value_name='hourTemp')
    dfNew['hour'] = dfNew['hour'].apply(lambda x: x[1:])
    dfNewT['hour'] = dfNewT['hour'].apply(lambda x: x[1:])
    dfNewTP = dfNewT.pivot_table(values='hourTemp', index=['year', 'month', 'day', 'date', 'hour'], columns="station_id").reset_index(['year', 'month', 'day', 'date', 'hour'])
    dfNewM = pd.merge(dfNew, dfNewTP, on=['date','hour'])

    c_names = {}
    for i in range(1,12):
        c_names[i] = 'station_'+str(i)

    c_names2 = {}
    for i in range(1, 21):
        c_names2[i] = 'zone_' + str(i)

    dfNewM.rename(columns=c_names, inplace=True)
    dfNewM.drop(['year_y','month_y','day_y','day_y'],inplace=True,axis=1,errors='ignore')
    dfNewM2 = dfNewM.pivot_table(values='hourLoad', index=['year_x', 'month_x', 'day_x', 'date', 'hour', 'station_1',
                                                             'station_2','station_3','station_4','station_5','station_6','station_7',
                                                             'station_8','station_9', 'station_10', 'station_11'], columns="zone_id").reset_index(['station_1',
                                                             'station_2','station_3','station_4','station_5','station_6','station_7',
                                                             'station_8','station_9', 'station_10', 'station_11'])
    dfNewM2.rename(columns=c_names2, inplace=True)

    dfNewM2['station_avg'] = dfNewM2['station_1'] / 12
    for i in range(1, 12):
        dfNewM2['station_avg'] = dfNewM2['station_avg'] + dfNewM2['station_' + str(i)] / 12

    dfNewM2['zone_avg'] = dfNewM2['zone_1'] / 20
    for i in range(1, 21):
        dfNewM2['zone_avg'] = dfNewM2['zone_avg'] + dfNewM2['zone_' + str(i)] / 20

    dfNewM2 = dfNewM2.reset_index(['date', 'hour'])
    dfNewM2['hour'] = dfNewM2['hour'].astype(int) - 1
    dfNewM2['hour'] = dfNewM2['hour'].astype(str).apply(lambda x: x.zfill(2))
    dfNewM2['date'] = dfNewM2['date'].astype(str) + " " + dfNewM2['hour'].astype(str) + ":00"
    dfNewM2.to_csv("allHours.csv")
    return dfNewM2

def init_dfs():
    df = pd.read_csv('all.csv', na_values=[''])
    dfHourly = pd.read_csv('allHours.csv', na_values=[''])
    #df = initDataFrame()
    #dfHourly = initDataFrameHourly()
    return df, dfHourly
