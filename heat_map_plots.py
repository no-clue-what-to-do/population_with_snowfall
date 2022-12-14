# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 12:19:52 2022

@author: i09300090
"""

import numpy as np
import pandas as pd   
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('talk')

from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import colors

from ease_lonlat import EASE2GRID, SUPPORTED_GRIDS


#%%load saved data
snow_data_north = pd.read_csv('combined_north.csv', index_col=0)
snow_data_south = pd.read_csv('combined_south.csv', index_col=0)


df_pop_north = pd.read_csv('pop_north_ease_grid.csv', index_col=0)
df_pop_south = pd.read_csv('pop_south_ease_grid.csv', index_col=0)

#%% convert grid points to latitude and longitude
grid_north = EASE2GRID(name='EASE2_N25km', **SUPPORTED_GRIDS['EASE2_N25km'])
grid_south = EASE2GRID(name='EASE2_S25km', **SUPPORTED_GRIDS['EASE2_S25km'])


num_rows = len(df_pop_north.index)
num_cols = len(df_pop_north.columns)

long_cols_north = []
lat_rows_north = []

long_cols_south = []
lat_rows_south = []

for col in range(num_rows):
    for row in range(num_cols):
        # pixel_center_long, pixel_center_lat = grid_north.rc2lonlat(col=col+1, row=row+1)
        
        # long_cols_north.append(pixel_center_long)
        # lat_rows_north.append(pixel_center_lat)

        pixel_center_long, pixel_center_lat = grid_south.rc2lonlat(col=col, row=row)
        
        long_cols_south.append(pixel_center_long)
        lat_rows_south.append(pixel_center_lat)
        

#%%

pop_cmap = 'Wistia'
snow_cmap = 'cool'

pop_data = np.log(df_pop_north[df_pop_north>0])
snow_data = np.log(snow_data_north)

# pop_data = df_pop_south
# snow_data = snow_data_south

#custom color map for population, colors get thrown off by ocean values being Nan
cmap = colors.Colormap('Wistia')
normalize = colors.Normalize(vmin=0, vmax=pop_data.max().max())


fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)
pop_im = ax1.imshow(pop_data,cmap=pop_cmap, norm=normalize)
ax1.axis('off')
ax1.set_title('World Population Heat Map')

###add colorbar to left side of first axis
divider = make_axes_locatable(ax1)
cax = divider.append_axes('left', size='2%', pad=.5)
cbar_1 = fig.colorbar(pop_im, cax=cax, orientation='vertical')
cbar_1.set_ticks([0, pop_data.max().max()])
cbar_1.set_ticklabels(['Low \nPopulation', 'High \nPopulation'])



ax2.imshow(pop_data,cmap=pop_cmap, norm=normalize)
snow_im = ax2.imshow(snow_data, cmap=snow_cmap)

ax2.axis('off')
ax2.set_title('Snow Amount Overlaid')

###add colorbar to right side of second axis

divider = make_axes_locatable(ax2)
cax = divider.append_axes('left', size='2%', pad=.5)
cbar_2 = fig.colorbar(snow_im, cax=cax, orientation='vertical')

cbar_2.set_ticks([0, snow_data.max().max()])
cbar_2.set_ticklabels(['Little \nSnow', 'Lots of \nSnow'])

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
#%%
plt.savefig('North_Pop_snow_fall_figure.png')
