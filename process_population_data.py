# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 14:42:43 2021

@author: Kevin Ludlum
"""

import tqdm
import rasterio


import numpy as np
import pandas as pd   
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('talk')


def plot_raster(arr, title=None, figsize=(30,10)):
    """ helper function to plot a raster array """
    fig, ax = plt.subplots(figsize=figsize)
    plt.imshow(arr)
    plt.colorbar()
    plt.title(f'{title}')
    plt.xlabel('Column #')
    plt.ylabel('Row #')
    return fig, ax

def get_population_count(vector_polygon,raster_layer):
  gtraster, bound = rasterio.mask.mask(raster_layer, [vector_polygon], crop=True)
  pop_estimate = gtraster[0][gtraster[0]>0].sum()
  return (pop_estimate.round(2))



#%%load population data
file = 'population_data_2020_1km_Aggregated.tif'
pop_raster = rasterio.open(file)

print('No. of bands:',(pop_raster.count))


#%%load snow data
snow_data_north = pd.read_csv('processed_data/combined_north.csv', index_col=0)
snow_data_south = pd.read_csv('processed_data/combined_south.csv', index_col=0)


#%%define window for pop data

#just northern hemisphere
# w = pop_raster.read(1, window=rasterio.windows.Window(0, 0, 50000, 18720/2))

#whole planet
w = pop_raster.read(1)

longitude, latitude  = pop_raster.xy(9000, 25000)
print(f'long:{longitude}, lat:{latitude}')

plot_raster(w)



#%% setup grids to convert longitude and latitude into grid row, col
from ease_lonlat import EASE2GRID, SUPPORTED_GRIDS
grid_north = EASE2GRID(name='EASE2_N25km', **SUPPORTED_GRIDS['EASE2_N25km'])
grid_south = EASE2GRID(name='EASE2_S25km', **SUPPORTED_GRIDS['EASE2_S25km'])


#%%loop to get pop data and convert it into EASE grid format
pop_north = np.zeros((721,721))
pop_south = np.zeros((721,721))
for i in tqdm.tqdm(range(w.shape[0])):
    for j in range(w.shape[1]):
        if w[i,j]>0:
            longitude, latitude  = pop_raster.xy(i,j)
            
            if latitude>=0:
    
                col, row = grid_north.lonlat2rc(lon=longitude, lat=latitude)
                
                pop_north[row,col] += w[i,j]
                
            if latitude<0:

                col, row = grid_south.lonlat2rc(lon=longitude, lat=latitude)
                
                pop_south[row,col] += w[i,j]
                

#%% save pop data as csv
df_pop_north = pd.DataFrame(pop_north)
df_pop_north.to_csv('processed_data/pop_north_ease_grid.csv')

df_pop_south = pd.DataFrame(pop_south)
df_pop_south.to_csv('processed_data/pop_south_ease_grid.csv')




