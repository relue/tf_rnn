# -*- coding: utf-8 -*-
'''Todos
- Simple Statistics für Energy Loads und Temperatures (Mean,Max,Min, Median) Schiefe, Streuung
- Aggregation nach Zeit auf Tage, Wochen, Monate (einfache Abfragen, Selects, Filter)
- Visualisierung der einzelnen Werte nach Zeit und als Boxplots, Histogramme, Kerndichteschätzung
- Scattersplots für Visualisierung der Korrelation/Matrix/Rangkorrleation?
- nach Außereisern und Missing Values suchen
- ggbf. imputation der missing values
- RNN Modell an Daten fitten
- verschiedene Hyperparameter Varianten identifizieren
'''

import pandas as pd
import numpy as np

df = pd.read_csv('energy_load/Load_history.csv', thousands=',', dtype='float')
df.h1 = df.h1.astype(float)
print df.dtypes
print df.head()
print df.describe("h1")



