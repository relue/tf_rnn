import pandas as pd

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
        "hiddenLayers": (1,5),
        "weightInit": ["zero", "one", "normal", "glorot_uniform", "lecun_uniform", "glorot_normal"],
        "useHoliday": [True, False],
        "useWeekday": [True, False],
}
errorBounds = {
        "val_rmse":  (19000 , 100000),
        "test_rmse": (140000,400000),
}
errorType = "test_rmse"
paramName = "standardizationType"

output_file('hyperparams.html')
dfNew = pd.read_pickle("randomSearch.pd")
x = dfNew[paramName].tolist()
y = dfNew[errorType].tolist()
p1 = figure(width=1000, height=500, y_range=(errorBounds[errorType][0],errorBounds[errorType][1]))#x_range = (defDict[paramName][0],defDict[paramName][1]),

p1.xaxis.axis_label = paramName
p1.yaxis.axis_label = "Loss "
r31 = p1.circle(x, y, color="red", size=2, alpha=0.6)

legend3 = Legend(legends=[
    (paramName+" and loss",   [r31])
], location=(40, 5))

p1.add_layout(legend3, 'below')

from bokeh.charts import BoxPlot,Histogram, Scatter

p = BoxPlot(dfNew, values='val_rmse', label='learningRate',title="MPG Summar", outliers=False)
p2 = Histogram(dfNew['timeWindow'], title="MPG Distribution")
p3 = Scatter(dfNew, x='timeWindow', y='val_rmse', title="HP vs MPG",
            xlabel="Miles Per Gallon", ylabel="Horsepower")


ap = gridplot([[p1], [p],[p2],[p3]])

show(ap)
