# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 12:38:22 2022

@author: Kevin Ludlum

Script is used to look up the population and snow fall results for specific cities

It does seem like snowfall is being undercounted, given that Ushuaia
shows zero snow as a result. It does have a pretty small popualtions though

Auckland and Mexico city show no snow, which I think is right.

And snowy places like Stockhold and southern germany
 do register snow and decent popualtions

Feel free to look up the longitude and latitude of a city or place
and add to the test!
"""


import rasterio
import pandas as pd   
from ease_lonlat import EASE2GRID, SUPPORTED_GRIDS


def city_test(longitude, latitude, conversion_grid, snow_df, raster_data, pop_data):
    indices = raster_data.index(longitude, latitude)
    
    population = pop_data[indices]

    col, row = conversion_grid.lonlat2rc(lon=longitude, lat=latitude)
    
    snow_amount = snow_df.iloc[row, col]
    

    
    return population, snow_amount
    
#%%load snow data
snow_data_north = pd.read_csv('processed_data/combined_snow_data_north.csv', index_col=0)
snow_data_south = pd.read_csv('processed_data/combined_snow_data_south.csv', index_col=0)

# plt.imshow(snow_data.values)


#%%define window for population data
file = 'ppp_2020_1km_Aggregated.tif'
pop_raster = rasterio.open(file)

print('No. of bands:',(pop_raster.count))
#just northern hemisphere
# w = pop_raster.read(1, window=rasterio.windows.Window(0, 0, 50000, 18720/2))

#whole planet
raster = pop_raster.read(1)

longitude, latitude  = pop_raster.xy(9000, 25000)
print(f'long:{longitude}, lat:{latitude}')

#%% define ease grid
grid_north = EASE2GRID(name='EASE2_N25km', **SUPPORTED_GRIDS['EASE2_N25km'])
grid_south = EASE2GRID(name='EASE2_S25km', **SUPPORTED_GRIDS['EASE2_S25km'])

#%% test points
###Mexico City
longitude, latitude =  -99.12, 19.45
population, snow_amount = city_test(longitude, latitude, grid_north, snow_data_north, pop_raster, raster)
print(f'Mexico City \nPopulation: {population}\nSnow Fall: {snow_amount}\n')


###Anchorage
longitude, latitude = -149.86, 61.2
population, snow_amount = city_test(longitude, latitude, grid_north, snow_data_north, pop_raster, raster)
print(f'Anchorage \nPopulation: {population}\nSnow Fall: {snow_amount}\n')


###Stockholm
longitude, latitude = 18.06, 59.33
population, snow_amount = city_test(longitude, latitude, grid_north, snow_data_north, pop_raster, raster)
print(f'Stockholm \nPopulation: {population}\nSnow Fall: {snow_amount}\n')


###Rome
longitude, latitude = 12.49, 41.9
population, snow_amount = city_test(longitude, latitude, grid_north, snow_data_north, pop_raster, raster)
print(f'Rome \nPopulation: {population}\nSnow Fall: {snow_amount}\n')


###Freiburg
longitude, latitude = 7.84, 48
population, snow_amount = city_test(longitude, latitude, grid_north, snow_data_north, pop_raster, raster)
print(f'Freiburg \nPopulation: {population}\nSnow Fall: {snow_amount}\n')


###Auckland
longitude, latitude = 174.76, -36.84
population, snow_amount = city_test(longitude, latitude, grid_south, snow_data_south, pop_raster, raster)
print(f'Auckland \nPopulation: {population}\nSnow Fall: {snow_amount}\n')


###Buenos Aires
longitude, latitude = -58.38, -34.60
population, snow_amount = city_test(longitude, latitude, grid_south, snow_data_south, pop_raster, raster)
print(f'Buenos Aires \nPopulation: {population}\nSnow Fall: {snow_amount}\n')


###Ushuaia
longitude, latitude = -68.3, -54.8
population, snow_amount = city_test(longitude, latitude, grid_south, snow_data_south, pop_raster, raster)
print(f'Ushuaia \nPopulation: {population}\nSnow Fall: {snow_amount}\n')


###Wanaka
longitude, latitude = 169.1, -44.7
population, snow_amount = city_test(longitude, latitude, grid_south, snow_data_south, pop_raster, raster)
print(f'Wanaka \nPopulation: {population}\nSnow Fall: {snow_amount}\n')
