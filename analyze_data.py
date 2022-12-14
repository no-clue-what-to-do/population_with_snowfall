# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 16:11:56 2022

@author: Kevin Ludlum
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%load snow data
snow_data_north = pd.read_csv('processed_data/combined_snow_data_north.csv', index_col=0)
snow_data_south = pd.read_csv('processed_data/combined_snow_data_south.csv', index_col=0)


#%% load population data
df_pop_north = pd.read_csv('processed_data/pop_north_ease_grid.csv', index_col=0)
df_pop_south = pd.read_csv('processed_data/pop_south_ease_grid.csv', index_col=0)


#%%calculate percent of population without snow

df_north = pd.DataFrame([df_pop_north.values.flatten(), snow_data_north.values.flatten()],
                       index=['population', 'snow']).T

pop_total_north = df_north['population'].sum()
no_snow_pop_north = df_north[df_north['snow']==0]['population'].sum()

percent_no_snow_north = 100*(no_snow_pop_north/pop_total_north)


df_south = pd.DataFrame([df_pop_south.values.flatten(), snow_data_south.values.flatten()],
                        index=['population', 'snow']).T

pop_total_south = df_south['population'].sum()
no_snow_pop_south = df_south[df_south['snow']==0]['population'].sum()

percent_no_snow_south = 100*(no_snow_pop_south/pop_total_south)


percent_no_snow = (no_snow_pop_north+no_snow_pop_south)/(pop_total_south+pop_total_north)


print(f'Percent of sane people: {100*percent_no_snow}')

#%%
long_north = pd.melt(df_pop_north, ignore_index=False,
        value_name='population', var_name='column').reset_index(level=0)

long_north['snow'] = pd.melt(snow_data_north)['value']

snow_folk_df = long_north[long_north['snow']!=0][long_north['population']!=0]

snow_folk_df[snow_folk_df['snow']<20]['population'].sum()

long_south = pd.melt(df_pop_south, ignore_index=False,
        value_name='population', var_name='column').reset_index(level=0)

#%%
#makes snowfall numbers yearly, nopt sum of 25 years
snow_folk_df['snow'] = snow_folk_df['snow']/25 

plt.figure()
sns.scatterplot(data=snow_folk_df, x='population', y='snow')
sns.despine()

plt.ylabel('Snow Water Equivalent (mm)')
plt.xlabel('Population')




#references:
# https://www.worldpop.org/geodata/summary?id=24777
# https://towardsdatascience.com/visualising-global-population-datasets-with-python-c87bcfc8c6a6
# https://medium.com/@danielmoyo/raster-data-in-python-part-ii-working-with-geographic-coordinates-a368708de5f2

#convert long/lat to ease grid
# https://pypi.org/project/ease-lonlat/
