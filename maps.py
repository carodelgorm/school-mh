"""This script creates maps of state-level school-based mental-health policies"""

import os
import io
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import matplotlib.colors as mcolors
from zipfile import ZipFile
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import FuncFormatter
from shapely.geometry import Polygon
import missingno as msno
from PIL import Image
from matplotlib.patches import Patch, Circle

from util.env import data_path, out_path

from plotting import set_properties, format_axes


def get_state_level_df():
    """
    This fcn merges state-level policy information with geodata for plotting
    """
    df = pd.read_csv(data_path('state_services.csv'))
    
    gdf = gpd.read_file(data_path('cb_2018_us_state_500k.zip')) 



if __name__ == '__main__':
    pass