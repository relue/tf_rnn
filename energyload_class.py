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
import dataExplore2
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

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
    dfNewM2.sort_values(['date'], ascending=[True], inplace=True)
    dfNewM2 = dfNewM2.dropna(subset = ['zone_1'])
    #dataExplore2.showDF(dfNewM2, True)

    dfNewM2.to_csv("allHours.csv")
    return dfNewM2

def init_dfs(create = False, all = True):
    if create:
        df = initDataFrame()
        dfHourly = initDataFrameHourly()
        dfHourly['date'] = pd.to_datetime(dfHourly['date'])
    else:
        dfHourly = pd.read_csv('allHours.csv', na_values=[''])
        dfHourly['date'] = pd.to_datetime(dfHourly['date'])
        if all:
            df = pd.read_csv('all.csv', na_values=[''])
            return df, dfHourly
        else:
            return dfHourly

def getBatch(gInput, gOutput, i, batchSize, isMLP):
    fromI = i*batchSize
    toI = fromI + batchSize
    if isMLP:
        inputR = gInput[fromI:toI,:]
    else:
        inputR = gInput[:,fromI:toI]
    return inputR, gOutput[fromI:toI]

def createX(df, featureList, save = False, isMLP = False, isLogarithmic = False, timeWindow = 1, jumpSequences = False):
    columns = range(timeWindow, -1, -1)
    if save:
        dfNew = pd.DataFrame(columns=columns)
        for i in range(0, len(df), timeWindow if jumpSequences else 1):#len(df.index)
            if i >= timeWindow:
                columnList = []
                for t in columns:
                    tupleList = []
                    for feature in featureList:
                        tupleList.append(df.iloc[i-t][feature])
                    columnList.append(tupleList)
                row=pd.Series(columnList,columns)
                dfNew = dfNew.append([row],ignore_index=True)
        dfNew[featureList] = dfNew[0].apply(pd.Series)
        dfNew.to_pickle("rnnInputOld.pd")
        #dataExplore2.showDF(dfNew, True)
        #dataExplore2.showDF(dfNew, True)
    else:
        dfNew = pd.read_pickle('rnnInputOld.pd')

    tfInput = []
    tfOutput= []
    embeddedInputColumns =[]
    if isLogarithmic:
        scaler = MinMaxScaler(feature_range=(0, 1))

    if isMLP:
        for t in columns:
            tempTuple = []
            for feature in featureList:
                tempTuple.append(feature+'_'+str(t))
                embeddedInputColumns.append(feature+'_'+str(t))
            dfNew[tempTuple] = dfNew[t].apply(pd.Series)
        tfInput = dfNew.loc[:,embeddedInputColumns]
        tfOutput = np.asarray(dfNew[featureList[-1]].tolist())
        #dataExplore2.showDF(tfInput, True)
    else:
        for t in columns:
            if t == 0:
                tfOutput = dfNew[featureList[-1]].tolist()
            else:
                if isLogarithmic:
                    scaledInputs = scaler.fit_transform(dfNew[t].tolist())
                else:
                    scaledInputs = dfNew[t].tolist()
                tfInput.append(scaledInputs)
    #[t, rows, inputs]

    tfInput= np.asarray(tfInput)
    tfOutput= np.asarray(tfOutput)
    if isLogarithmic:
        scaler = MinMaxScaler(feature_range=(0, 1))
        return tfInput, scaler.fit_transform(tfOutput), scaler
    else:
        return tfInput,tfOutput

def createXmulti(df, timeWindow, station_id, zone_id, outputSize, save = False, isStandardized = False):
    columns = range(1, timeWindow+1)
    dfS = df[["zone_"+str(zone_id),"station_"+str(station_id)]]
    if isStandardized:
        scalerOutput = MinMaxScaler(feature_range=(0, 1))
        scalerInput = MinMaxScaler(feature_range=(0, 1))

        scaledLoads = scalerOutput.fit_transform(dfS["zone_"+str(zone_id)].tolist())
        lo = pd.Series(scaledLoads)
        dfS["zone_"+str(zone_id)] = lo.values

        scaledTemps = scalerInput.fit_transform(dfS["station_"+str(station_id)].tolist())
        te = pd.Series(scaledTemps)
        dfS["station_"+str(station_id)] = te.values

    if save:
        dfNew = pd.DataFrame(columns=columns)
        for i in range(0, len(dfS), outputSize):#len(df.index)
            if i >= timeWindow and i+outputSize < len(df):
                columnList = []
                for t in columns:
                    tupleList = []
                    tupleList.append(dfS.iloc[i-t]["zone_"+str(zone_id)])
                    tupleList.append(dfS.iloc[i-t]["station_"+str(station_id)])
                    columnList.append(tupleList)
                    outputList = []
                    for o in range(0, outputSize):
                        outputList.append(dfS.iloc[i+o]["zone_"+str(zone_id)])
                row=pd.Series(columnList+[outputList],columns+["output"])
                dfNew = dfNew.append([row],ignore_index=True)
        #dfNew[featureList] = dfNew[0].apply(pd.Series)
        dfNew.to_pickle("rnnInput.pd")
        #dataExplore2.showDF(dfNew, False)
    else:
        dfNew = pd.read_pickle('rnnInput.pd')
        #dataExplore2.showDF(dfNew, False)



    tfOutput = np.asarray(dfNew["output"].tolist())
    tfInput = []
    for t in columns:
        tfInput.append(dfNew[t].tolist())
    #[t, rows, inputs]

    tfInput= np.asarray(tfInput)
    if isStandardized:
        return tfInput, tfOutput, scalerOutput
    else:
        return tfInput,tfOutput
