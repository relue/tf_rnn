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
        "l1Penalty": (0.0001, 0.01),

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
        "val_loss":  (0 , 1),
        "test_loss": (140000,300000),

}
errorType = "test_loss"
paramName = "hiddenNodes"

output_file('hyperparams.html')
dfNew = pd.read_pickle("randomSearch.pd")
x = dfNew[paramName].tolist()
y = dfNew[errorType].tolist()
p1 = figure(width=1000, height=500, x_range = (defDict[paramName][0],defDict[paramName][1]), y_range=(errorBounds[errorType][0],errorBounds[errorType][1]))

p1.xaxis.axis_label = paramName
p1.yaxis.axis_label = "Loss "
r31 = p1.circle(x, y, color="red", size=10, alpha=0.1)

legend3 = Legend(legends=[
    (paramName+" and loss",   [r31])
], location=(40, 5))

p1.add_layout(legend3, 'below')

ap = gridplot([[p1]])

show(ap)
