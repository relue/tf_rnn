import pandas as pd
import experimentConfig
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

from bokeh.charts import BoxPlot

defDict = {
        "learningRate":  (0 , 1),
        "DropoutProp": (0.01, 0.99),
        "l1Penalty": (0.0001, 0.99),
        "standardizationType": ["minmax", "zscore"],
        "activationFunction": ["tanh", "sigmoid", "relu"],
        "hiddenNodes": (10,300),
        "optimizer":  ['adam', 'sgd', 'rms','ada', 'adadelta'],
        "timeWindow": (10,199),
        "batchSize": (1,101),
        "hiddenLayers": (1,10),
        "weightInit": ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"],
        "useHoliday": [True, False],
        "useWeekday": [True, False],
}
errorBounds = {
        "val_rmse":  (19000 , 100000),
        "test_rmse": (140000,400000),
}
toPlot = ["learningRate", "hiddenLayers", "timeWindow", "hiddenNodes", "l1Penalty", "standardizationType", "activationFunction", "optimizer", "batchSize", "weightInit", "useHoliday", "useWeekday"]
c = experimentConfig.Config()
errorType = "test_rmse"

dfNew = pd.read_pickle("randomSearch.pd")
output_file('hyperparams.html')
l_params = []

for paramName in toPlot:
    isDiscrete = c.parameterTypeDiscrete[paramName]

    x = dfNew[paramName].tolist()
    y = dfNew[errorType].tolist()
    y2 = dfNew["exec_time"].tolist()
    if not isDiscrete:
        p1 = figure(width=500, height=500, y_range=(errorBounds[errorType][0],errorBounds[errorType][1]))#x_range = (defDict[paramName][0],defDict[paramName][1]),
        p1.xaxis.axis_label = paramName
        p1.yaxis.axis_label = errorType
        r31 = p1.circle(x, y, color="red", size=2, alpha=0.6)
        legend3 = Legend(legends=[
            (paramName+" and "+errorType,   [r31])
        ], location=(40, 5))
        p1.add_layout(legend3, 'below')

        p2 = figure(width=500, height=500, y_range=(0,2000))#x_range = (defDict[paramName][0],defDict[paramName][1]),
        p2.xaxis.axis_label = paramName
        p2.yaxis.axis_label = "execution time"
        r31 = p2.circle(x, y2, color="red", size=2, alpha=0.6)
        legend3 = Legend(legends=[
            (paramName+" and execution time",   [r31])
        ], location=(40, 5))
        p2.add_layout(legend3, 'below')

    else:
        p1 = BoxPlot(dfNew, values=errorType, label=paramName,title=paramName+" and "+errorType, outliers=False)
        p1.xaxis.axis_label = paramName
        p1.yaxis.axis_label = errorType

        p2 = BoxPlot(dfNew, values="exec_time", label=paramName,title=paramName+" and execution time", outliers=False)
        p2.xaxis.axis_label = paramName
        p2.yaxis.axis_label = "execution time"


    l_params.append([p1,p2])

ap = gridplot(l_params)
show(ap)
