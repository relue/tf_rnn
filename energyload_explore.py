# -*- coding: utf-8 -*-
'''Todos
- Simple Statistics für Energy Loads und Temperatures (Mean,Max,Min, Median) Schiefe, Streuung
- Aggregation nach Zeit auf Tage, Wochen, Monate (einfache Abfragen, Selects, Filter)
- Visualisierung der einzelnen Werte nach Zeit und als Boxplots, Histogramme, Kerndichteschätzung
- Scattersplots für Visualisierung der Korrelation/Matrix/Rangkorrleation?
- nach Ausreisern und Missing Values suchen
- ggbf. imputation der missing values
- RNN Modell an Daten fitten
- verschiedene Hyperparameter Varianten identifizieren
Was ist das wichtigste? Temp Durchschnitte über Zeit Stunden (Uhrzeit) und Wochentag, Monat
- 1x Durchschnitte Temp und Load für Agg Uhrzeit -> check
- 1x "" für Wochentag
- 1x "" für Monat
optional convert nach fahrenheit
- verläufe pro zone -> nein
- korrelierende Zonen?

+ pro Wochentag
+ pro Monat
+ Korrelation

Transformation bzw Impute von Missing Values?

Neue Todos:
- Korrelation Heatmap
- einfaches RNN
- transformierte Daten überprüfen
-
'''

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

dfHourly['date'] = pd.to_datetime(dfHourly['date'])
output_file('diagrams1.html')

tempList = []
loadList = []
for i in range(1, 25):
    tempList.append(df[['c'+str(i)]].mean(axis=0))

for i in range(1, 25):
    loadList.append(df[['h'+str(i)+'_x']].mean(axis=0))



#
# Durchschnitte Temp und Load für Agg-Uhrzeit
#
p = figure(width=1000, height=500, x_range=(0, 24), y_range=(-10, 40),
                toolbar_location="left")

p.xaxis.axis_label = "Hour of Daytime"
p.yaxis.axis_label = "Temperature in Celsius"

r0 = p.line(range(1, 25), tempList, color="red", line_width=2)
r1 = p.circle(range(1, 25), tempList, color="red")
p.extra_y_ranges = {"foo": Range1d(start=40000, end=100000)}

r2 = p.line(range(1, 25), loadList, color="blue", line_width=2, y_range_name="foo")
r3 = p.circle(range(1, 25), loadList, color="blue", y_range_name="foo")

legend = Legend(legends=[
    ("Avg. Temperature in Celsius",   [r0, r1]),
    ("Avg. Energy Load", [r2, r3])
], location=(40, 5))

p.add_layout(LinearAxis(y_range_name="foo", axis_label="Energy Load"), 'right')
p.add_layout(legend, 'below')

#
# Durchschnitte Temp und Load für Agg-Uhrzeit
#
# Liste aus Datumsangaben Strings
# Liste mit Daily Loads
df['date'] = pd.to_datetime(df['date'])
df['dayLoad'] = df['dayLoad'] / 24
df['dayTemp'] = df['dayTemp'] / 24
dfAggE = df.groupby(['date'], as_index = False)['dayLoad'].mean()
dfAggT = df.groupby(['date'], as_index = False)['dayTemp'].mean()

p2 = figure(width=1000, height=500, y_range=(dfAggT['dayTemp'].min(),dfAggT['dayTemp'].max()),
                toolbar_location="left")

p2.xaxis.axis_label = "Date"
p2.yaxis.axis_label = "Temperature "
p2.yaxis[0].formatter = PrintfTickFormatter(format="%5.1f C")
p2.xaxis.formatter=DatetimeTickFormatter(formats=dict(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    ))
p2.xaxis.major_label_orientation = pi/4

r20 = p2.line(dfAggT['date'], dfAggT['dayTemp'], color="red", line_width=0.5, line_alpha = 0.8)
# r21 = p2.circle(dfAggT['date'], dfAggT['dayTemp'], color="red")

r22 = p2.line(dfAggE['date'], dfAggE['dayLoad'], color="blue", line_width=0.5, y_range_name="foo", line_alpha = 0.8)
# r23 = p2.circle(dfAggE['date'], dfAggE['dayLoad'], color="blue", y_range_name="foo")
p2.extra_y_ranges = {"foo": Range1d(start=dfAggE['dayLoad'].min(), end=dfAggE['dayLoad'].max())}

legend2 = Legend(legends=[
    ("Avg. Temperature in Celsius",   [r20]),
    ("Avg. Energy Load", [r22])
], location=(40, 5))

ax = LinearAxis(y_range_name="foo", axis_label="Energy Load")
ax.formatter = PrintfTickFormatter(format="%5.0f V")
p2.add_layout(ax, 'right')
p2.add_layout(legend2, 'below')

#
# Durchschnitte Temp und Load für Wochentag
#
# Liste aus Datumsangaben Strings
# Liste mit Daily Loads

df['weekday'] = pd.DatetimeIndex(df['date']).weekday

dfAggE = df.groupby(['weekday'], as_index = False)['dayLoad'].mean()
dfAggT = df.groupby(['weekday'], as_index = False)['dayTemp'].mean()
dfAggE['weekname'] = dfAggE['weekday'].apply(lambda x: calendar.day_name[x])
dfAggT['weekname'] = dfAggT['weekday'].apply(lambda x: calendar.day_name[x])

p3 = figure(width=1000, height=500, x_range = dfAggT['weekname'].tolist(), y_range=(dfAggT['dayTemp'].min(),dfAggT['dayTemp'].max()))

p3.xaxis.axis_label = "Date"
p3.yaxis.axis_label = "Temperature "
p3.yaxis[0].formatter = PrintfTickFormatter(format="%5.1f C")

r30 = p3.line(dfAggT['weekname'], dfAggT['dayTemp'], color="red", line_width=0.5, line_alpha = 0.8)
r31 = p3.circle(dfAggT['weekname'], dfAggT['dayTemp'], color="red")

r32 = p3.line(dfAggE['weekname'], dfAggE['dayLoad'], color="blue", line_width=0.5, y_range_name="foo", line_alpha = 0.8)
r33 = p3.circle(dfAggE['weekname'], dfAggE['dayLoad'], color="blue", y_range_name="foo")
p3.extra_y_ranges = {"foo": Range1d(start=dfAggE['dayLoad'].min(), end=dfAggE['dayLoad'].max())}

legend3 = Legend(legends=[
    ("Avg. Temperature in Celsius",   [r30, r31]),
    ("Avg. Energy Load", [r32, r33])
], location=(40, 5))

ax = LinearAxis(y_range_name="foo", axis_label="Energy Load")
ax.formatter = PrintfTickFormatter(format="%5.0f V")
p3.add_layout(ax, 'right')
p3.add_layout(legend3, 'below')

#
# Durchschnitte Temp und Load für Wochentag
#
# Liste aus Datumsangaben Strings
# Liste mit Daily Loads

dfAggE = df.groupby(['month_x'], as_index = False)['dayLoad'].mean()
dfAggT = df.groupby(['month_x'], as_index = False)['dayTemp'].mean()
dfAggE['monthname'] = dfAggE['month_x'].apply(lambda x: calendar.month_name[int(x)])
dfAggT['monthname'] = dfAggT['month_x'].apply(lambda x: calendar.month_name[int(x)])

p4 = figure(width=1000, height=500, x_range = dfAggT['monthname'].tolist(), y_range=(dfAggT['dayTemp'].min(),dfAggT['dayTemp'].max()))

p4.xaxis.axis_label = "Date"
p4.yaxis.axis_label = "Temperature "
p4.yaxis[0].formatter = PrintfTickFormatter(format="%5.1f C")

r30 = p4.line(dfAggT['monthname'], dfAggT['dayTemp'], color="red", line_width=0.5, line_alpha = 0.8)
r31 = p4.circle(dfAggT['monthname'], dfAggT['dayTemp'], color="red")

r32 = p4.line(dfAggE['monthname'], dfAggE['dayLoad'], color="blue", line_width=0.5, y_range_name="foo", line_alpha = 0.8)
r33 = p4.circle(dfAggE['monthname'], dfAggE['dayLoad'], color="blue", y_range_name="foo")
p4.extra_y_ranges = {"foo": Range1d(start=dfAggE['dayLoad'].min(), end=dfAggE['dayLoad'].max())}

legend3 = Legend(legends=[
    ("Avg. Temperature in Celsius",   [r30, r31]),
    ("Avg. Energy Load", [r32, r33])
], location=(40, 5))

ax = LinearAxis(y_range_name="foo", axis_label="Energy Load")
ax.formatter = PrintfTickFormatter(format="%5.0f V")
p4.add_layout(ax, 'right')
p4.add_layout(legend3, 'below')

#
# Scatterplot daily basis

df1 = df[['dayLoad','dayTemp']]

p5 = figure(width=1000, height=500, x_range = (df1['dayLoad'].min(),df1['dayLoad'].max()), y_range=(df1['dayTemp'].min(),df1['dayTemp'].max()))

p5.xaxis.axis_label = "Energy Load"
p5.yaxis.axis_label = "Temperature "
p5.yaxis[0].formatter = PrintfTickFormatter(format="%5.1f C")
r31 = p5.circle(df1['dayLoad'], df1['dayTemp'], color="red", size=0.5)

legend3 = Legend(legends=[
    ("Avg. Temperature in Celsius",   [r31])
], location=(40, 5))

p5.add_layout(legend3, 'below')

#
# Scatterplot hourly basis


p6 = figure(width=1000, height=500, x_range = (dfHourly['zone_avg'].min(),dfHourly['zone_avg'].max()), y_range=(dfHourly['station_avg'].min(),dfHourly['station_avg'].max()))

p6.xaxis.axis_label = "Date"
p6.yaxis.axis_label = "Temperature "
p6.yaxis[0].formatter = PrintfTickFormatter(format="%5.1f C")
r31 = p6.circle(dfHourly['zone_avg'], dfHourly['station_avg'], color="red", size=0.5)

legend3 = Legend(legends=[
    ("Avg. Temperature in Celsius",   [r31])
], location=(40, 5))

p6.add_layout(legend3, 'below')

ap = gridplot([[p],[p2], [p3], [p4], [p5], [p6]])


show(ap)




