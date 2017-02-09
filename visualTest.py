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

import energyload_class
df, dfHourly = energyload_class.init_dfs()
output_file('test.html')
dfHourly['x'] = dfHourly['zone_1']
dfHourly['y'] = dfHourly['station_1']
# Individual Scatterplot
source = ColumnDataSource(dfHourly)

p8 = figure(width=1000, height=500)

p8.xaxis.axis_label = "Energy Load"
p8.yaxis.axis_label = "Temperature "
r31 = p8.circle("x", "y", color="red", size=0.5, source=source)

codeX = """

var x = cb_obj.get('value');
var data = source.get('data');
zone_x = data[x];

for (i = 0; i < zone_x.length; i++) {
        data['x'][i] = zone_x[i];
    }
source.trigger('change');

"""

codeY = """

var y = cb_obj.get('value');
var data = source.get('data');
station_y = data[y];
for (i = 0; i < station_y.length; i++) {
        data['y'][i] = station_y[i];
    }
source.trigger('change');

"""

callbackx = CustomJS(args=dict(source=source), code=codeX)
callbacky = CustomJS(args=dict(source=source), code=codeY)

c_names = []
for i in range(1,12):
    c_names.append(('Station '+str(i), 'station_'+str(i)))

c_names2 = []
for i in range(1, 21):
    c_names2.append(('Zone ' + str(i), 'zone_' + str(i)))

menu0 = c_names2
dropdown0 = Dropdown(label="Zones", type="warning", menu=menu0)
dropdown0.js_on_change('value', callbackx)

menu = c_names
dropdown = Dropdown(label="Stations", type="warning", menu=menu)
dropdown.js_on_change('value', callbacky)


#data_table = getBokehTable(corr)
#show(data_table)

ap = gridplot([[p8, dropdown, dropdown0]])


show(ap)
