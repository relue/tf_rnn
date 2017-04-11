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

output_file('hyperparams.html')
dfNew = pd.read_pickle("randomSearch.pd")
print dfNew
x = dfNew["l1Penalty"].tolist()
y = dfNew["loss"].tolist()
p1 = figure(width=1000, height=500, x_range = (x.min(),x.max()), y_range=(y.min(),y.max()))

p1.xaxis.axis_label = "L1Penalty"
p1.yaxis.axis_label = "Loss "
r31 = p1.circle(x, y, color="red", size=0.5)

legend3 = Legend(legends=[
    ("L1Penalty and Loss",   [r31])
], location=(40, 5))

p1.add_layout(legend3, 'below')

ap = gridplot([[p1]])

show(ap)