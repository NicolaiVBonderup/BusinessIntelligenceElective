import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io_handler as io
import os
from pandas import Series

def generate_scatter_plot(dataframe):
    plot = dataframe.plot(kind='scatter',x='lon',y='lat')
    plot.get_figure().savefig('latlongscatter.png')