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

from plotting import set_properties


def get_state_level_df() -> pd.DataFrame:
    """
    This fcn merges state-level policy information with geodata for plotting
    """
    df = pd.read_csv(data_path('state_level_policies.csv'))
    df = df.drop('state', axis=1)
    
    gdf = gpd.read_file(data_path('cb_2018_us_state_500k.zip')) 

    gdf = gdf.merge(df,left_on='STUSPS', right_on='abbrev')

    return gdf


def plot_colored_map(gdf: pd.DataFrame, 
                     var: str, 
                     color: str,
                     suptitle: str, 
                     title: str, 
                     note_text: str, 
                     save:bool = False):
        
    set_properties()

    fig, ax = plt.subplots(1, figsize=(18, 14))
    ax.axis('off')

    fig.suptitle(suptitle,
                 fontsize=16, ha='left', 
                 x=0.1, y=0.86, 
                 fontweight='bold', 
                 color='#20222e',)
    fig.text(0.1, 0.81,
             title,
             fontsize=18, ha='left',
             fontweight='bold', 
            color='#20222e',
            )

    get_mainland(gdf=gdf, var=var, color=color, ax=ax)

    get_alaska(gdf=gdf, var=var, fig=fig, ax=ax)

    get_hawaii(gdf=gdf, var=var, fig=fig, ax=ax)

    if var == 'prek12_sel':
        legend_handles = [
            Patch(facecolor='#E8F6F3', edgecolor='#E8F6F3', label='Pre-K Only'),
            Patch(facecolor='#A2D9CE', edgecolor='#A2D9CE', label='Pre-K and Early Education'),
            Patch(facecolor='#45B39D', edgecolor='#45B39D', label='Pre-K through High School')
        ]
        ax.legend(handles=legend_handles, loc='lower right', fontsize=12, title_fontsize=14)

    ax.annotate(
        note_text, 
        xy=(0.07, .08), 
        xycoords='figure fraction', 
        fontsize=12, 
        color='#aeb0b7'
        )
    
    fig.patch.set_facecolor('#e8ecfc')
    ax.set_facecolor('#e8ecfc')

    if save==True:
        plt.savefig(out_path(f'map_{var}.png'), dpi=300, bbox_inches='tight')
    else:
        plt.show()


def makeColorColumn(gdf: pd.DataFrame, variable: str, color_for_y: str) -> pd.DataFrame:
    # Create a color mapping based on specific conditions
    if variable == 'prek12_sel':
        color_map = {
            'pre_k': '#E8F6F3',
            'pre_k_ee': '#A2D9CE',
            'pre_k_12': '#45B39D'
        }
    else:
        color_map = {
            'No': 'whitesmoke',  # Color for 'n' vals
            'Yes': color_for_y,  # Color for 'y' vals 
        }
    # Apply the color mapping to the dataframe, defaulting to 'white' if val is not defined
    gdf['map_color'] = gdf[variable].apply(lambda x: color_map.get(x, 'white'))
    
    return gdf


def get_mainland(gdf: pd.DataFrame, var: str, color: str, ax):
    
    gdf = makeColorColumn(gdf, var, color)

    # Create "visframe" as a re-projected gdf using EPSG 2163
    visframe = gdf.to_crs(epsg=2163)

    # Plot states sans Hawaii and Alaska using 'map_color' col
    visframe[
    ~visframe['STUSPS'].isin(
        ['HI', 'AK']
    )].plot(
        ax=ax,
        color=visframe['map_color'][~visframe['STUSPS'].isin(['HI', 'AK'])],
        linewidth=0.8,edgecolor='0.8'
    )
    if 0:
        for idx, row in visframe.iterrows():
            x, y = row['geometry'].centroid.coords[0]  # Get the centroid of the polygon
            ax.annotate(text=row['STUSPS'], xy=(x, y), ha='center', va='center')

    return

def get_alaska(gdf: pd.DataFrame, var, fig, ax):
    
    akax = fig.add_axes([0.1, 0.17, 0.2, 0.19])   
    akax.axis('off')
    
    ak_polygon = Polygon([(-170,50),(-170,72),(-140, 72),(-140,50)])
    
    alaska_gdf = gdf[gdf['STUSPS']=='AK']
    
    alaska_gdf.clip(ak_polygon).plot(
        color=gdf[gdf['STUSPS']=='AK']['map_color'], 
        linewidth=0.8,ax=akax, 
        edgecolor='0.8')

    return


def get_hawaii(gdf: pd.DataFrame, var, fig, ax):    
    
    hiax = fig.add_axes([.28, 0.20, 0.1, 0.1])   
    hiax.axis('off')
    
    hi_polygon = Polygon([(-160,0),(-160,90),(-120,90),(-120,0)])
    hawaii_gdf = gdf[gdf['STUSPS']=='HI']
    
    hawaii_gdf.clip(hi_polygon).plot(
        column=var, 
        color=gdf[gdf['STUSPS']=='HI']['map_color'], 
        linewidth=0.8,ax=hiax, 
        edgecolor='0.8'
    )

    return


if __name__ == '__main__':
    gdf = get_state_level_df()


    plot_colored_map(
        gdf=gdf, 
        var='mh_literacy', 
        color='#2fa8ff',
        suptitle='Appendix Figure 2', 
        title='States with laws requiring mental health literacy in schools as of 2021',
        note_text='Source: School Mental Health Policy Map, https://theshapesystem.com/. Accessed 26 June 2024',
        save=True
        )

    plot_colored_map(
        gdf=gdf, 
        var="mh_absences", 
        color="#e60049",
        suptitle="Appendix Figure 3", 
        title="States with laws requiring mental health excused school absenses as of 2024",
        note_text="Source: Author's compilation of state laws as of 31 August 2024",
        save=True
        )
    
    plot_colored_map(
        gdf=gdf, 
        var="prek12_sel", 
        color="#e60049",
        suptitle="Appendix Figure 4", 
        title="States laws requiring social-emotional learning programs as of 2020",
        note_text="Source: School Mental Health Policy Map, https://theshapesystem.com/. Accessed 26 June 2024",
        save=True
        )
