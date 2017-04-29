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

from bokeh.charts import BoxPlot

errorBounds = {
        "val_rmse":  (13000 , 24000),
        "test_rmse": (80000,170000),
}
toPlot = ["epochSize", "learningRate", "hiddenLayers", "timeWindow", "hiddenNodes",
          "l1Penalty", "activationFunction", "optimizer", "batchSize",
          "weightInit", "DropoutProp"]#"standardizationType","useHoliday", "useWeekday"
#toPlot = []
c = experimentConfig.Config()
errorType = "val_rmse"
errorType2 = "test_rmse"
isSensi = False

plotWhat = "rand_1"
plotWhat = "tpe_1"
#errorBounds = {"val_rmse":  (23000 , 26000), "test_rmse": (170000,190000)}
#plotWhat = "manualSensi"
plotWhat = "tpe_2"
plotWhat = "tpe_2b"
plotWhat = "tpe_3"

#plotWhat = "sensi_tpe_3"
plotWhat = "sensi2_tpe_3" #3
#optWhat = "tpe_3"
optWhat = "tpe_4"
plotWhat = "tpe_4"
isSensi = True

if isSensi == True:
    alpha = 1
    size = 2
    rangeY = None
    rangeY = (errorBounds[errorType][0], errorBounds[errorType][1])
    rangeY2 = (errorBounds[errorType2][0], errorBounds[errorType2][1])
    #sensiObj = c.sensiExperiment1
    bestDict = c.getBestAsDict(optWhat, hypeOnly=False, orderByIndexID=False)
    bestDictHypes = c.getBestAsDict(optWhat, hypeOnly=True, orderByIndexID=False)
else:
    bestDict = c.getBestAsDict(plotWhat, hypeOnly=False, orderByIndexID=False)
    bestDictHypes = c.getBestAsDict(plotWhat, hypeOnly=True, orderByIndexID=False)
    alpha = 0.3
    size = 1
    rangeY = (errorBounds[errorType][0], errorBounds[errorType][1])
    rangeY2 = (errorBounds[errorType2][0], errorBounds[errorType2][1])

dfNew = pd.read_pickle("searchResults/"+plotWhat+".pd")

l_params = []
#dfNew.dropna(axis=1, how='all')
dfNew = dfNew.fillna(0)
dfNewPlain = dfNew.sort_index()
minError = 999999999
minList = []
valListMin = []
testListMin = []
genIndex = []
i = 1
for row in dfNewPlain.itertuples():

    if not math.isnan(row.val_rmse):
        if row.val_rmse < minError:
            valListMin.append(row.val_rmse)
            testListMin.append(row.test_rmse)
            genIndex.append(i)
        minError = min(row.val_rmse, minError)
        minList.append(minError)
        i += 1
dfNewPlain['min'] = minList

pSearch = figure(title=u"Optimizer Durchlaeufe und Validation RMSE", width=500, height=500, y_range= (errorBounds[errorType][0], errorBounds[errorType][1]))
pSearch.line(dfNewPlain.index, dfNewPlain['min'], color="red", line_width=1, line_alpha = 1)
pSearch.circle(dfNewPlain.index, dfNewPlain['val_rmse'], color="blue", size=2, alpha = 0.5)
pSearch.xaxis.axis_label = "Runs"
pSearch.yaxis.axis_label = "Validation RMSE"

pSearch2 = figure(title=u"Optimizer Durchlaeufe und Test RMSE",width=500, height=500, y_range= (errorBounds[errorType2][0], errorBounds[errorType2][1]))
pSearch2.circle(dfNewPlain.index, dfNewPlain['test_rmse'], color="red", size=2, alpha = 0.5)
pSearch2.xaxis.axis_label = "Runs"
pSearch2.yaxis.axis_label = "Test RMSE"

pSearch3 = figure(title=u"Optimizer und neue gefunde Minima Validation RMSE",width=500, height=500, y_range= (errorBounds[errorType][0], errorBounds[errorType][1]))
pSearch3.circle(genIndex, valListMin, color="blue")
pSearch3.xaxis.axis_label = "Runs"
pSearch3.yaxis.axis_label = "Validation RMSE"

pSearch4 = figure(title=u"Generalisierung Test RMSE fuer gefundene Validation RMSE Minima",width=500, height=500, y_range= (errorBounds[errorType2][0], errorBounds[errorType2][1]))
pSearch4.circle(genIndex, testListMin, color="red")
pSearch4.xaxis.axis_label = "Runs"
pSearch4.yaxis.axis_label = "Test RMSE"


output_file('bokehPlots/'+plotWhat+'_optimizeProgress.html')

pname = []
pvalue = []
for keys in bestDictHypes:
    pname.append(keys)
    pvalue.append(bestDictHypes[keys])
columns = [TableColumn(field="Parameter", title="Parameter"), TableColumn(field="Wert", title="Wert")]
tDict = {"Parameter": pname, "Wert": pvalue}
data = ColumnDataSource(tDict)
dTable = DataTable(source=data, columns=columns, width=400, height=580)
tb = widgetbox(dTable)
l_params.append([pSearch, pSearch2])
l_params.append([pSearch3, pSearch4])
ap = gridplot(l_params)
save(ap)

l_params = []
i = 1
h = 1
tools = "pan,wheel_zoom,box_zoom,reset, hover"
for paramName in toPlot:
    isDiscrete = c.parameterTypeDiscrete[paramName]

    i += 1
    x = dfNew[paramName].tolist()

    y = dfNew[errorType].tolist()
    y2 = dfNew[errorType2].tolist()
    y3 = dfNew["exec_time"].tolist()

    xRange = None
    if isDiscrete:
        isNumeric = c.parameterNumeric
        if not paramName in isNumeric.keys():
            xRange = c.experimentConfigWide[paramName]
            x = [str(x[i]) for i in range(len(x))]

    points = []
    pList = []
    if True:
        p1 = figure(width=500, height=500, tools=tools, x_range=xRange,y_range=rangeY) #x_range = (defDict[paramName][0],defDict[paramName][1]),
        p1.xaxis.axis_label = paramName
        p1.yaxis.axis_label = errorType
        p1.circle(source=dfNew, x=paramName, y=errorType, color="red", size=size, alpha=alpha)

        if True:
            r = p1.circle(x=[bestDict[paramName]],y=[bestDict[errorType]], color="blue", size=5, alpha=1)
            legend3 = Legend(legends=[
                ("found optimum for "+str(bestDict[paramName]),   [r])
            ], location=(40, 5))
            p1.add_layout(legend3, 'below')
        pList.append(p1)

        p2 = figure(width=500, height=500, tools=tools,x_range=xRange,y_range=rangeY2) #x_range = (defDict[paramName][0],defDict[paramName][1]),
        p2.xaxis.axis_label = paramName
        p2.yaxis.axis_label = errorType2
        r = p2.circle(source=dfNew, x=paramName, y=errorType2, color="red", size=size, alpha=alpha)

        if True:
            r = p2.circle(x=[bestDict[paramName]], y=[bestDict[errorType2]], color="blue", size=6, alpha=1)

            legend3 = Legend(legends=[
                ("found optimum for " + str(bestDict[paramName]), [r])
            ], location=(40, 5))
            p2.add_layout(legend3, 'below')
        pList.append(p2)

        if isSensi == False:
            p3 = figure(width=500, height=500, tools=tools, x_range=xRange)#x_range = (defDict[paramName][0],defDict[paramName][1]),
            p3.xaxis.axis_label = paramName
            p3.yaxis.axis_label = "execution time"
            r31 = p3.circle(x, y3, color="red", size=size, alpha=alpha)
            legend3 = Legend(legends=[
                (paramName+" and execution time",   [r31])
            ], location=(40, 5))
            p3.add_layout(legend3, 'below')
            pList.append(p3)
        pList.append(tb)
    else:
        '''
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


