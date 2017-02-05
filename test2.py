import pandas as pd

from bokeh.charts import HeatMap, bins, output_file, show
from bokeh.layouts import column, gridplot
from bokeh.palettes import RdYlGn6, RdYlGn9
from bokeh.sampledata.autompg import autompg
from bokeh.sampledata.unemployment1948 import data

# setup data sources
data = data.copy()
data['Year'] = data['Year'].astype(str)
unempl = pd.melt(data, var_name='Month', value_name='Unemployment', id_vars=['Year'])

fruits = {'fruit': ['apples', 'apples', 'apples', 'apples', 'apples',
                    'pears', 'pears', 'pears', 'pears', 'pears',
                    'bananas', 'bananas', 'bananas', 'bananas', 'bananas'],
          'fruit_count': [4, 5, 8, 12, 4, 6, 5, 4, 8, 7, 1, 2, 4, 8, 12],
          'year': [2009, 2010, 2011, 2012, 2013, 2009, 2010, 2011, 2012, 2013, 2009, 2010,
                   2011, 2012, 2013]}
fruits['year'] = [str(yr) for yr in fruits['year']]

hm9 = HeatMap(fruits, y='year', x='fruit', values='fruit_count', stat=None)

output_file("heatmap.html", title="heatmap.py example")

show(hm9)