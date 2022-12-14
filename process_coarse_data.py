# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 17:13:36 2022

@author: Kevin Ludlum
"""
import os
import struct

import numpy as np
import pandas as pd   
import matplotlib.pyplot as plt

from functools import reduce

def read_single_NSIDC8(file):
    '''code to open and convert format of NSIDC8 from here:
        https://nsidc.org/data/nsidc-0271/versions/1'''
    with open(file, 'rb') as f:
        contents = f.read()
    
    converted_data = []
    for i in range(len(contents)):
        if i%2==0:
            converted_data.append(struct.unpack("<h", contents[i:i+2])[0])
    
    grid_results = np.asarray(converted_data).reshape(721,721)
    
    return pd.DataFrame(grid_results)


#%% process the different folders of snow_ north data, and make it a single dataframe
local_folder = os.path.dirname(os.path.realpath(__file__))

folders = [os.path.join(local_folder,
                        r'raw_snow_data\nsidc0271v01.n.1978-1987\north\1978-1987'),                        
           os.path.join(local_folder,
                        r'raw_snow_data\nsidc0271v01.n.1987-2003\north\1987-2003')]


north_snow_data = []
for folder in folders:
    df_temp_list = []
    for file in os.listdir(folder):
        if file.endswith(".NSIDC8"):
            file_name = os.path.join(folder, file)
            print(file)
            results = read_single_NSIDC8(file_name)
            
            results[results < 0] = 0 ##only psoitive values correspond to snow amounts
            ###see data user guide
            
            df_temp_list.append(results)
    
    
    sum_df = reduce(lambda x, y: x.add(y), df_temp_list)
        
    north_snow_data.append(sum_df)

combined_north = reduce(lambda x, y: x.add(y), df_temp_list)
combined_north.to_csv('processed_data/combined_snow_data_north.csv')
plt.imshow(combined_north)



#%% same thing for the south data

folders =[ r'C:\Users\i13500020\.spyder-py3\Snow\coarse data\nsidc0271v01.s.1978-1987\south\1978-1987',
          r'C:\Users\i13500020\.spyder-py3\Snow\coarse data\nsidc0271v01.s.1987-2003\south\1987-2003']

south_snow_data = []
for folder in folders:
    df_temp_list = []
    for file in os.listdir(folder):
        if file.endswith(".NSIDC8"):
            file_name = os.path.join(folder, file)
            print(file)
            results = read_single_NSIDC8(file_name)
            
            results[results < 0] = 0 ##only psoitive values correspond to snow amounts
            ###see data user guide
            
            df_temp_list.append(results)
    
    
    sum_df = reduce(lambda x, y: x.add(y), df_temp_list)
        
    south_snow_data.append(sum_df)

combined_south = reduce(lambda x, y: x.add(y), df_temp_list)
combined_south.to_csv('processed_data/combined_snow_data_south.csv')
plt.imshow(combined_south)


