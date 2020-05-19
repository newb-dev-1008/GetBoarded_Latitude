import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

#reading the csv file
df=pd.read_csv('corrected_covid_data.csv')

#grouping data according to countries
new_df=df.groupby('Country/Region').max()

#transferring grouped data to usingthis csv file
new_df.to_csv('usingthis.csv')

#creating final dataframe for plotting
countries=list(new_df.index)
recoveries=list(new_df['Recovered'])
latitude=list(new_df['Latitude'])
longitude=list(new_df['Longitude'])
avgt=list(new_df['Average Temperature'])
avgh=list(new_df['Average Humidity'])
cases={'Countries':countries,'Recoveries':recoveries,'Latitude':latitude,'Longitude':longitude,'Avg.Temperature':avgt,'Avg.Humidity':avgh}
final_df=pd.DataFrame.from_dict(cases)

#final dataframe transferred to constraintsdata.csv
final_df.to_csv('constraintsdata.csv')

#creating map
world=open('world.json','r').read()
world_map=folium.Map(location=[0,0],zoom_start=4)

for lat,lon,rec,temp,humid in zip(final_df['Latitude'],final_df['Longitude'],final_df['Recoveries'],final_df['Avg.Temperature'],final_df['Avg.Humidity']):
    folium.Marker(location=[lat,lon],popup=(rec,temp,humid)).add_to(world_map)
folium.Choropleth(geo_data=world,
                     data=final_df,
                     columns=['Countries','Recoveries'],
                     key_on='feature.properties.name',
                     fill_color='PuRd',
                     fill_capacity=0.7,
                     line_opacity=0.2,
                     legend_name='Recoveries with weather').add_to(world_map)

#map saved to weather.html
world_map.save(outfile='weather.html')
