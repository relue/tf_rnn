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
output_file('diagrams1.html')

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
source = ColumnDataSource(dfHourly)

p8 = figure(width=1000, height=500, x_range = (dfHourly['zone_1'].min(),dfHourly['zone_1'].max()), y_range=(dfHourly['station_1'].min(),dfHourly['station_1'].max()))

p8.xaxis.axis_label = "Energy Load"
p8.yaxis.axis_label = "Temperature "
r31 = p8.circle("zone_1", "station_1", color="red", size=0.5, source=source)

legend3 = Legend(legends=[
    ("Avg. Temperature in Celsius",   [r31])
], location=(40, 5))

p8.add_layout(legend3, 'below')


def callback(source=source):
    data = source.get('data')
    zone_1, station_1 = data['zone_1'], data['station_2']
    for i in range(len(zone_1)):
        station_1[i] = 20
    source.trigger('change')

menu = [("Item 1", "1"), ("Item 2", "2"), None, ("Item 3", "3")]
dropdown = Dropdown(label="Dropdown button", type="warning", menu=menu, callback=CustomJS.from_py_func(callback))

#data_table = getBokehTable(corr)
#show(data_table)

ap = gridplot([[p8, dropdown], [hm1, hm2], [hm3, None]])


show(ap)
