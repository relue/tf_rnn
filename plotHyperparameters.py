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

from bokeh.charts import BoxPlot

errorBounds = {
        "val_rmse":  (14000 , 25000),
        "test_rmse": (110000,180000),
}
toPlot = ["epochSize", "learningRate", "hiddenLayers", "timeWindow", "hiddenNodes",
          "l1Penalty", "standardizationType", "activationFunction", "optimizer", "batchSize",
          "weightInit", "useHoliday", "useWeekday"]
#toPlot = []
c = experimentConfig.Config()
errorType = "val_rmse"
errorType2 = "test_rmse"

plotWhat = "rand_1"
#plotWhat = "tpe_1"
plotWhat = "manualSensi"
isSensi = True
if isSensi == True:
    alpha = 1
    size = 2
    rangeY = None
    sensiObj = c.sensiExperiment1
else:
    alpha = 0.3
    size = 1
    rangeY = (errorBounds[errorType][0], errorBounds[errorType][1])

dfNew = pd.read_pickle("searchResults/"+plotWhat+".pd")
l_params = []

dfNewPlain = dfNew.sort_index()
minError = 999999999
minList = []
for row in dfNewPlain.itertuples():
    if not math.isnan(row.val_rmse):
        minError = min(row.val_rmse, minError)
    minList.append(minError)
dfNewPlain['min'] = minList

pSearch = figure(width=500, height=500)
pSearch.line(dfNewPlain.index, dfNewPlain['min'], color="red", line_width=0.5, line_alpha = 0.8)
pSearch.xaxis.axis_label = "Runs"
pSearch.yaxis.axis_label = "Minimum Error"

output_file('bokehPlots/'+plotWhat+'_optimizeProgress.html')
l_params.append([pSearch, None])
ap = gridplot(l_params)
save(ap)

l_params = []
i = 1
h = 1
for paramName in toPlot:
    isDiscrete = c.parameterTypeDiscrete[paramName]
    i += 1
    x = dfNew[paramName].tolist()
    y = dfNew[errorType].tolist()
    y2 = dfNew[errorType2].tolist()
    y3 = dfNew["exec_time"].tolist()
    points = []
    if True:
        p1 = figure(width=500, height=500, y_range=rangeY) #x_range = (defDict[paramName][0],defDict[paramName][1]),
        p1.xaxis.axis_label = paramName
        p1.yaxis.axis_label = errorType
        r = p1.circle(x, y, color="red", size=size, alpha=alpha)
        points.append(r)
        if isSensi:
            r = p1.circle(x, y, color="blue", size=size, alpha=alpha)
            points.append(r)
        legend3 = Legend(legends=[
            (paramName+" and "+errorType,   points)
        ], location=(40, 5))
        p1.add_layout(legend3, 'below')

        p2 = figure(width=500, height=500, y_range=rangeY) #x_range = (defDict[paramName][0],defDict[paramName][1]),
        p2.xaxis.axis_label = paramName
        p2.yaxis.axis_label = errorType2
        r31 = p2.circle(x, y2, color="red", size=size, alpha=alpha)
        legend3 = Legend(legends=[
            (paramName+" and "+errorType2,   [r31])
        ], location=(40, 5))
        p2.add_layout(legend3, 'below')

        p3 = figure(width=500, height=500, y_range=rangeY)#x_range = (defDict[paramName][0],defDict[paramName][1]),
        p3.xaxis.axis_label = paramName
        p3.yaxis.axis_label = "execution time"
        r31 = p3.circle(x, y3, color="red", size=size, alpha=alpha)
        legend3 = Legend(legends=[
            (paramName+" and execution time",   [r31])
        ], location=(40, 5))
        p3.add_layout(legend3, 'below')

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


    l_params.append([p1, p2, p3])
    if i % 1 == 0:
        output_file('bokehPlots/'+plotWhat+'_'+paramName+'.html')
        ap = gridplot(l_params)
        save(ap)
        l_params = []
        h += 1

#output_file('bokehPlots/hyperparams'+str(h)+'.html')
#ap = gridplot(l_params)
#show(ap)


