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
import os.path

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

def getHolidayDict():
    dfHo = pd.read_csv('energy_load/Holiday_List.csv', sep=',')
    dfHo = pd.melt(dfHo, id_vars='dayName', var_name='year', value_name='date')
    dfHo = dfHo.dropna()
    dfHo['date'] = dfHo['year']+ "-"+ dfHo['date']
    dfHo['date'] = pd.to_datetime(dfHo['date'])
    holidayList = dfHo['date'].tolist()
    holidayDict = dict((el.date(),1) for el in holidayList)
    return holidayDict

def initDataFrameHourly():
    df = pd.read_csv('energy_load/Load_history.csv', thousands=',', dtype='float', na_values=[''])
    dfT = pd.read_csv('energy_load/temperature_history.csv', thousands=',', dtype='float', na_values=[''],sep=';')
    dfLoadS = pd.read_csv('energy_load/Load_solution.csv', dtype='float', sep=',')
    df = pd.concat([df, dfLoadS])



    #dataExplore2.showDF(df, False)
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
    for i in range(1, 22):
        c_names2[i] = 'zone_' + str(i)

    dfNewM.rename(columns=c_names, inplace=True)
    dfNewM.drop(['year_y','month_y','day_y','day_y'],inplace=True,axis=1,errors='ignore')
    dfNewM2 = dfNewM.pivot_table(values='hourLoad', index=['year_x', 'month_x', 'day_x', 'date', 'hour', 'station_1',
                                                             'station_2','station_3','station_4','station_5','station_6','station_7',
                                                             'station_8','station_9', 'station_10', 'station_11'], columns="zone_id").reset_index(['station_1',
                                                             'station_2','station_3','station_4','station_5','station_6','station_7',
                                                             'station_8','station_9', 'station_10', 'station_11'])
    dfNewM2.rename(columns=c_names2, inplace=True)

    dfNewM2['station_avg'] = dfNewM2['station_1'] / 11
    for i in range(1, 12):
        dfNewM2['station_avg'] = dfNewM2['station_avg'] + dfNewM2['station_' + str(i)] / 11
    dfNewM2['station_12'] = dfNewM2['station_avg']
    dfNewM2['zone_avg'] = dfNewM2['zone_1'] / 20
    for i in range(1, 21):
        dfNewM2['zone_avg'] = dfNewM2['zone_avg'] + dfNewM2['zone_' + str(i)] / 20

    dfNewM2 = dfNewM2.reset_index(['date', 'hour'])
    dfNewM2['hour'] = dfNewM2['hour'].astype(int) - 1
    dfNewM2['hour'] = dfNewM2['hour'].astype(str).apply(lambda x: x.zfill(2))
    dfNewM2['date'] = dfNewM2['date'].astype(str) + " " + dfNewM2['hour'].astype(str) + ":00"
    dfNewM2.sort_values(['date'], ascending=[True], inplace=True)
    dfNewM2 = dfNewM2.dropna(subset = ['zone_1'])
    dfNewM2['date'] = pd.to_datetime(dfNewM2['date'])
    # def alert(d,holidayDict):
    #     if d['date'].date() in holidayDict:
    #         return 1
    #     else:
    #         return 0
    # dfNewM2['isHoliday'] = dfNewM2.apply((lambda x: alert(x, holidayDict)),  axis=1)
    #dataExplore2.showDF(dfNewM2, False)
    #dataExplore2.showDF(dfNewM2, False)
    dfNewM2.to_csv("allHours.csv")
    return dfNewM2

def init_dfs(create = False, all = True):
    if create:
        df = initDataFrame()
        dfHourly = initDataFrameHourly()
        dfHourly['date'] = pd.to_datetime(dfHourly['date'])
        return dfHourly
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

def getHolidayVector(date, holidayDict):
    holidayVector = []
    for i in range(0,7):
        nextDay = date + pd.DateOffset(i)
        if nextDay.date() in holidayDict:
            isIn = 1
        else:
            isIn = 0
        holidayVector.append(isIn)
    return holidayVector

def createInputOutputRow(dfS, i, columns, zoneColumns, stationColumns, outputSize, holidayDict, addSystemLevel = False,
                         noFillZero = True, useHoliday = True, useWeekday = True):
    columnList = []
    futureTemps = []
    outputList = []

    for o in range(0, outputSize):
        timeRowOutput = dfS.ix[i+o]
        #for station_name in stationColumns:
            #futureTemps.append(dfS.ix[i+o][station_name])
        for zone_name in zoneColumns:
            outputList.append(timeRowOutput[zone_name])
        if addSystemLevel:
            outputList.append(timeRowOutput["zone_21"])

    for t in columns:
        tupleList = []
        timeRowInput = dfS.ix[i-t]
#        tupleList.append(dfS.ix[i-t]['date'])
        for zone_name in zoneColumns:
            tupleList.append(timeRowInput[zone_name])
        for station_name in stationColumns:
            tupleList.append(timeRowInput[station_name])
        #tupleList += futureTemps

        if t == 1 or noFillZero == True:
            holidayVector = getHolidayVector(timeRowInput["date"], holidayDict)
            weekDayVector = []
            for d in range(0,7):
                weekDayVector.append(timeRowInput[d])
        else:
            holidayVector = [0] * len(holidayVector)
            weekDayVector = [0] * len(weekDayVector)

        if useHoliday:
            tupleList+=holidayVector

        if useWeekday:
            tupleList+=weekDayVector

        columnList.append(tupleList)
    row=pd.Series(columnList+[outputList],columns+["output"])
    return row

def createXmulti(df, timeWindow, stationIDs, outputSize, save = False, isStandardized = False, noFillZero = False, useHoliday = True, useWeekday = True):
    columns = range(1, timeWindow+1)
    zoneIDs = range(1,21)
    holidayDict = getHolidayDict()
    zoneColumns = ["zone_" + str(i) for i in zoneIDs]
    stationColumns = ["station_" + str(i) for i in stationIDs]
    df['weekday'] = df['date'].dt.dayofweek

    dfS = df[zoneColumns+stationColumns+["date","weekday"]]
    dfDummy = pd.get_dummies(dfS['weekday'])
    dfS = pd.concat([dfS, dfDummy], axis=1)
    #dataExplore2.showDF(dfS, False)
    if isStandardized:
        scalerOutput = MinMaxScaler(feature_range=(0, 1))
        scalerInput = MinMaxScaler(feature_range=(0, 1))

        for zone_name in zoneColumns:
            scaledLoads = scalerOutput.fit_transform(dfS[zone_name].tolist())
            lo = pd.Series(scaledLoads)
            dfS[zone_name] = lo.values

        for station_name in stationColumns:
            scaledTemps = scalerInput.fit_transform(dfS[station_name].tolist())
            lo = pd.Series(scaledTemps)
            dfS[station_name] = lo.values

    cacheAdd = ""
    cacheAdd += 'noFillZero' if noFillZero else ''
    cacheAdd += 'useHoliday' if useHoliday else ''
    cacheAdd += 'useWeekday' if useWeekday else ''

    cacheIdent = str(timeWindow) + "_" + str(outputSize)+"_"+cacheAdd
    filename = "rnnInputs/rnnInput"+str(cacheIdent)+".pd"
    cacheExists = os.path.isfile(filename)
    if save or not(cacheExists):
        dfNew = pd.DataFrame(columns=columns)
        for i in range(0, len(dfS), 24):#len(df.index)
            if i >= timeWindow and i+outputSize < len(df):
                row = createInputOutputRow(dfS, i, columns, zoneColumns, stationColumns, outputSize, holidayDict, noFillZero=noFillZero, useHoliday=useHoliday, useWeekday=useWeekday)
                dfNew = dfNew.append([row],ignore_index=True)
        #dfNew[featureList] = dfNew[0].apply(pd.Series)

        dfNew.to_pickle(filename)
        #dataExplore2.showDF(dfNew, False)
    else:
        dfNew = pd.read_pickle(filename)
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
