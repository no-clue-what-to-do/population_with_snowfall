Population With Snowfall

Article found here:
https://medium.com/@krludlum/its-really-weird-to-live-where-it-snows-a48c7dea191b

A little bit of code trying to estimate how much of the world popualtion lives in a place where it snows by combining gridded popualtion and snow data.

All of the snow data is uploaded to the git page, but the population datafile is huge, so it can be found and downloaded here: https://hub.worldpop.org/geodata/summary?id=24777

If, however, you trust my inital loading and reformatting of the data, you can simply use the files in the processed_data folder and check my results in the analyze_data.py script

test_individual_cities.py was my way to run a dummy test on the data. I just put the longitude and latitude of several famous cities to see if the snow and population numbers made sense. Feel free to add new locations to see if the data seems right

Besides that, heat_map_plots.py was the script used to make the heat map figures in the article