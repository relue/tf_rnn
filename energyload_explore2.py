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
output_file('diagrams2.html')

### Correlation Heatmap

c_names = []
for i in range(1,12):
    c_names.append('station_'+str(i))

c_names2 = []
for i in range(1, 21):
    c_names2.append('zone_' + str(i))

def getCorrHeatMap(df, xColList, yColList):
    corr = df.corr()
    zones = []
    stations = []
    values = []
    for r in itertools.product(xColList, yColList):
        zones.append(r[1])
        stations.append(r[0])
        values.append(corr.at[r[0],r[1]])

    heatData = {'x': zones,
              'values': values,
              'y': stations}

    return HeatMap(heatData, y='y', x='x', values='values', stat=None)

hm1 = getCorrHeatMap(dfHourly, c_names, c_names2)
hm2 = getCorrHeatMap(dfHourly, c_names, c_names)
hm3 = getCorrHeatMap(dfHourly, c_names2, c_names2)
hm4 = getCorrHeatMap(dfHourly.loc[dfHourly['station_avg'] > 15], c_names, c_names2)
hm5 = getCorrHeatMap(dfHourly.loc[dfHourly['station_avg'] <= 15], c_names, c_names2)

### Korrelationsmatrix
def getBokehTable(df):
    source = ColumnDataSource(df)
    columns = []
    for c in list(df.columns.values):
        tc = TableColumn(field=c, title=c)
        columns.append(tc)
    data_table = DataTable(source=source, columns=columns, width=2300, fit_columns=True)
    return data_table

dfHourly = dfHourly.set_index(["year_x", "month_x", "day_x", "hour"])
corr = dfHourly.corr()
corr.index.name = "ind"
corr = corr.reset_index("ind")

### Temperatures
'''
p7 = figure(width=800, height=700, y_range=(dfHourly['station_avg'].min(),dfHourly['station_avg'].max()))

p7.xaxis.axis_label = "Date"
p7.yaxis.axis_label = "Temperature "
p7.yaxis[0].formatter = PrintfTickFormatter(format="%5.1f C")
p7.xaxis.formatter=DatetimeTickFormatter(formats=dict(
        hours=["%d %B %Y %H"],
        days=["%d %B %Y %H"],
        months=["%d %B %Y %H"],
        years=["%d %B %Y %H"],
    ))
p7.xaxis.major_label_orientation = pi/4

lLegend = []
for i in range(1, 12):
    ref = p7.line(dfHourly['date'], dfHourly['station_'+str(i)], line_width=0.5, line_alpha = 0.8)
    lLegend.append(("Temperature for Station "+str(i),   [ref]))

legend2 = Legend(legends=lLegend, location=(30, 5))
p7.add_layout(legend2, 'right')
'''
c_names = []
for i in range(1,12):
    c_names.append('station_'+str(i))
'''
tsline = TimeSeries(dfHourly,
    x='date', y=c_names,
    color=c_names,
    title="Stations", ylabel='Temperatur', legend=True)
'''


# Individual Scatterplot
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

ap = gridplot([[dropdown0, dropdown], [p8, None], [hm1, hm2], [hm3, None], [hm4, hm5]])

show(ap)
