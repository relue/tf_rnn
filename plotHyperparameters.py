# coding=utf-8
import pandas as pd
import experimentConfig
from bokeh.charts import Bar, output_file, show
from bokeh.plotting import figure, show, output_file, save
from bokeh.sampledata.autompg import autompg as df
from bokeh.models import LinearAxis, Range1d
from bokeh.models import Legend
from bokeh.io import output_file, show, vplot, gridplot
from bokeh.models import DatetimeTickFormatter
from bokeh.models import PrintfTickFormatter
from bokeh.charts import HeatMap, output_file, show, TimeSeries
import itertools
import calendar
import math
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Dropdown
from bokeh.layouts import widgetbox
from bokeh.models import FixedTicker
from numpy import pi
from bokeh.charts import BoxPlot
import six

errorBounds = {
        "val_rmse":  (10000 , 15000),
        "test_rmse": (13700,17000),
        "val_mape":  (0.0 , 0.30),
        "test_mape": (0.0,0.30),
}
toPlot = ["epochSize", "learningRate", "hiddenLayers", "timeWindow", "hiddenNodes",
          "l1Penalty", "activationFunction", "optimizer", "batchSize",
          "weightInit", "DropoutProp", "standardizationType", "useHoliday", "useWeekday" ]#,"useHoliday", "useWeekday"
#toPlot = []
c = experimentConfig.Config()
errorType = "val_rmse"
errorType2 = "test_rmse"
#errorType = "val_mape"
#errorType2 = "test_mape"
isSensi = False
paramLabel = {}
errorLabel = {}
errorLabel[errorType] = "RMSE Validation-Set"
errorLabel[errorType2] = "RMSE Test-Set"
paramLabel["epochSize"] = "Anzahl der Epochen"
paramLabel["learningRate"] = "Learning Rate"
paramLabel["hiddenLayers"] = "Hidden Layers"
paramLabel["timeWindow"] = "Time Window Size"
paramLabel["hiddenNodes"] = "Anzahl der Hidden Nodes"
paramLabel["l1Penalty"] = "L1 Penalty"
paramLabel["activationFunction"] = "Aktivierungsfunktion"
paramLabel["optimizer"] = "Optimizer"
paramLabel["batchSize"] = "Batch Size"
paramLabel["weightInit"] = "Weight Initialization"
paramLabel["DropoutProp"] = "Dropout Probability"
paramLabel["standardizationType"] = "Standardisierungsmethode"
paramLabel["useHoliday"] = "Input Feiertage"
paramLabel["useWeekday"] = "Input Wochentage"

#plotWhat = "rand_1"
#plotWhat = "tpe_1"
#errorBounds = {"val_rmse":  (23000 , 26000), "test_rmse": (170000,190000)}

#plotWhat = "tpe_2"
#plotWhat = "tpe_2b"
#plotWhat = "tpe_3"

#plotWhat = "sensi_tpe_3"
#plotWhat = "sensi2_tpe_3" #3
#optWhat = "tpe_3"
#optWhat = "tpe_4"
#plotWhat = "tpe_4"
#isSensi = True
#plotWhat = "rand_2"

optWhat = "sensi_manual3"
plotWhat = "sensi_manual3"
#optWhat = "sensi_tpe_4"
#plotWhat = "sensi_tpe_4"
#optWhat = "sensi_test"
#plotWhat = "sensi_test"
isSensi = True
plotWidth = 450
plotHeight = 450

if isSensi == True:
    alpha = 1
    size = 4
    rangeY = None
    rangeY = (errorBounds[errorType][0], errorBounds[errorType][1])
    rangeY2 = (errorBounds[errorType2][0], errorBounds[errorType2][1])
    #sensiObj = c.sensiExperiment1
    bestDict = c.getBestAsDict(optWhat, hypeOnly=False, orderByIndexID=True)
    bestDictHypes = c.getBestAsDict(optWhat, hypeOnly=True, orderByIndexID=True)
    labelRedDots = "Ergebnis aus Sensitivitäts-Analyse"
else:
    bestDict = c.getBestAsDict(plotWhat, hypeOnly=False, orderByIndexID=False)
    bestDictHypes = c.getBestAsDict(plotWhat, hypeOnly=True, orderByIndexID=False)
    alpha = 0.35
    size = 2
    rangeY = (errorBounds[errorType][0], errorBounds[errorType][1])
    rangeY2 = (errorBounds[errorType2][0], errorBounds[errorType2][1])
    labelRedDots = "Beobachteter Parameter des TPE-Optimizers "

dfNew = pd.read_pickle("searchResults/"+plotWhat+".pd")

l_params = []
dfNew = dfNew.dropna()
dfNewPlain = dfNew.sort_index()
minError = 999999999
minErrorTest = 999999999
minList = []
minListTest = []
valListMin = []
testListMin = []
testListMin2 = []
genIndex = []
i = 1
for row in dfNewPlain.itertuples():
    if not math.isnan(row.val_rmse):
        if row.val_rmse < minError:
            valListMin.append(row.val_rmse)
            testListMin.append(row.test_rmse)
            genIndex.append(i)
        if row.test_rmse < minError:
            testListMin2.append(row.test_rmse)
        minError = min(row.val_rmse, minError)
        minErrorTest = min(row.test_rmse, minErrorTest)
        minList.append(minError)
        minListTest.append(minErrorTest)
        i += 1
dfNewPlain['min'] = minList
dfNewPlain['mintest'] = minListTest

pSearch = figure(width=plotWidth, height=plotHeight, y_range= (errorBounds[errorType][0], errorBounds[errorType][1])) #title=u"Optimizer Durchlaeufe und Validation RMSE",
pSearch.line(dfNewPlain.index, dfNewPlain['min'], color="blue", line_width=1, line_alpha = 1)
pSearch.circle(dfNewPlain.index, dfNewPlain['val_rmse'], color="blue", size=2, alpha = 0.7)
pSearch.xaxis.axis_label = "Anzahl der Durchläufe"
pSearch.yaxis.axis_label = errorLabel[errorType]

pSearch2 = figure(width=plotWidth, height=plotHeight, y_range= (errorBounds[errorType2][0], errorBounds[errorType2][1]))#title=u"Optimizer Durchlaeufe und Test RMSE",
pSearch2.line(dfNewPlain.index, dfNewPlain['mintest'], color="red", line_width=1, line_alpha = 1)
pSearch2.circle(dfNewPlain.index, dfNewPlain['test_rmse'], color="red", size=2, alpha = 0.7)
pSearch2.xaxis.axis_label = "Anzahl der Durchläufe"
pSearch2.yaxis.axis_label = errorLabel[errorType2]

pSearch3 = figure(width=plotWidth, height=plotHeight, y_range= (errorBounds[errorType][0], errorBounds[errorType][1])) #title=u"Optimizer und neue gefunde Minima Validation RMSE"
pSearch3.line(genIndex, valListMin, color="blue")
pSearch3.circle(genIndex, valListMin, color="blue")
pSearch3.xaxis.axis_label = "Anzahl der Durchläufe"
pSearch3.yaxis.axis_label = errorLabel[errorType]

pSearch4 = figure(width=plotWidth, height=plotHeight, y_range= (errorBounds[errorType2][0], errorBounds[errorType2][1])) #title=u"Generalisierung Test RMSE fuer gefundene Validation RMSE Minima",
pSearch4.line(genIndex, testListMin, color="red")
pSearch4.circle(genIndex, testListMin, color="red")
pSearch4.xaxis.axis_label = "Anzahl der Durchläufe"
pSearch4.yaxis.axis_label = errorLabel[errorType2]

output_file('bokehPlots/'+plotWhat+'_optimizeProgress.html')

pname = []
pvalue = []
for keys in bestDictHypes:
    pname.append(keys)
    pvalue.append(bestDictHypes[keys])
columns = [TableColumn(field="Parameter", title="Parameter"), TableColumn(field="Wert", title="Wert")]
tDict = {"Parameter": pname, "Wert": pvalue}
data = ColumnDataSource(tDict)
dTable = DataTable(source=data, columns=columns, width=300, height=400)
tb = widgetbox(dTable)
l_params.append([pSearch, pSearch2])
l_params.append([pSearch3, pSearch4])
ap = gridplot(l_params)
save(ap)

l_params = []
i = 1
h = 1
tools = "pan,wheel_zoom,box_zoom,reset, hover, save"
for paramName in toPlot:
    isDiscrete = c.parameterTypeDiscrete[paramName]
    if isSensi:
        if isinstance(bestDict[paramName], six.string_types):
            compStr = "'"+ bestDict[paramName] + "'"
        else:
            compStr = repr(bestDict[paramName])

        strQuery = paramName+ " != "+compStr
        print strQuery
        dfNewFiltered = dfNew.query(strQuery)
    else:
        dfNewFiltered = dfNew
    i += 1
    x = dfNewFiltered[paramName].tolist()

    y = dfNewFiltered[errorType].tolist()
    y2 = dfNewFiltered[errorType2].tolist()
    y3 = dfNewFiltered["exec_time"].tolist()

    xRange = None
    if isDiscrete:
        isNumeric = c.parameterNumeric
        if not paramName in isNumeric.keys():
            xRange = c.experimentConfigWide[paramName]
            x = [str(x[i]) for i in range(len(x))]

    points = []
    pList = []
    if True:
        p1 = figure(width=plotWidth, height=plotHeight, tools=tools, x_range=xRange,y_range=rangeY) #x_range = (defDict[paramName][0],defDict[paramName][1]),
        p1.xaxis.axis_label = paramLabel[paramName]
        if paramName == 'hiddenLayers':
            p1.xaxis[0].ticker = FixedTicker(ticks=range(1,11))
        if paramName == 'useWeekday':
            p1.xaxis[0].ticker = FixedTicker(ticks=[1,0])
        if paramName == 'useHoliday':
            p1.xaxis[0].ticker = FixedTicker(ticks=[0,1])
        if paramName == 'weightInit':
            p1.xaxis.major_label_orientation = pi / 4
        p1.yaxis.axis_label = errorLabel[errorType]
        paramNameFiltered = paramName
        #del paramNameFiltered[paramName]
        s= p1.circle(source=dfNewFiltered, x=paramName, y=errorType, color="red", size=size, alpha=alpha)

        if True:
            r = p1.circle(x=[bestDict[paramName]],y=[bestDict[errorType]], color="blue", size=7, alpha=1)
            legend3 = Legend(legends=[
                ("Gefundenes Optimum",   [r]),
                (labelRedDots, [s])
            ], location=(70, -60))
            p1.add_layout(legend3, 'above')
        pList.append(p1)

        p2 = figure(width=plotWidth, height=plotHeight, tools=tools,x_range=xRange,y_range=rangeY2) #x_range = (defDict[paramName][0],defDict[paramName][1]),
        p2.xaxis.axis_label = paramLabel[paramName]
        p2.yaxis.axis_label = errorLabel[errorType2]
        s = p2.circle(source=dfNewFiltered, x=paramName, y=errorType2, color="red", size=size, alpha=alpha)

        if True:
            r = p2.circle(x=[bestDict[paramName]], y=[bestDict[errorType2]], color="blue", size=7, alpha=1)
            legend3 = Legend(legends=[
                ("Gefundenes Optimum bei", [r]),
                (labelRedDots, [s])
            ], location=(40, 5))
            #p2.add_layout(legend3, 'below')
        pList.append(p2)
    '''
        if isSensi == False:
            p3 = figure(width=plotWidth, height=plotHeight, tools=tools, x_range=xRange)#x_range = (defDict[paramName][0],defDict[paramName][1]),
            p3.xaxis.axis_label = paramName
            p3.yaxis.axis_label = "execution time"
            r31 = p3.circle(x, y3, color="red", size=size, alpha=alpha)
            legend3 = Legend(legends=[
                (paramName+" and execution time",   [r31])
            ], location=(40, 5))
            p3.add_layout(legend3, 'below')
            pList.append(p3)
        

    else:
        
        p1 = BoxPlot(dfNew, values=errorType, label=paramName,title=paramName+" and "+errorType, outliers=False, legend=False)
        p1.xaxis.axis_label = paramName
        p1.xaxis.major_label_orientation = math.pi / 4
        p1.yaxis.axis_label = errorType

        p2 = BoxPlot(dfNew, values=errorType2, label=paramName,title=paramName+" and "+errorType2, outliers=False, legend=False)
        p2.xaxis.axis_label = paramName
        p2.yaxis.axis_label = errorType2

        p3 = BoxPlot(dfNew, values="exec_time", label=paramName,title=paramName+" and execution time", outliers=False, legend=False)
        p3.xaxis.axis_label = paramName
        p3.yaxis.axis_label = "execution time"
        
    '''
    pList.append(tb)
    l_params.append(pList)
    if i % 1 == 0:
        output_file('bokehPlots/'+plotWhat+'_'+paramName+'.html')
        ap = gridplot(l_params)
        save(ap)
        l_params = []
        h += 1

#output_file('bokehPlots/hyperparams'+str(h)+'.html')
#ap = gridplot(l_params)
#show(ap)


