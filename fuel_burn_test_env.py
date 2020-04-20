# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:56:06 2020

@author: agbon
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##key data 
distance_lower_bound = np.array([0, 801, 2001, 5501])
distance_upper_bound = np.array([800, 2000, 5500, 20000])    
fuel_burn = np.array([2.4, 3.42, 7.57, 6.29])   
passengers = np.array([136, 180, 291, 572])

pass_load_factor = 0.8 ##passenger load factor
kg_co2_kg_fuel = 3.15 #emissions per kg fuel burnt
inefficiencies = 0.1 #re-routing inefficiencies
fuel_lifecycle = 0.5064 #(kg CO2 / kg fuel)
GHG_m = 1.5 #GHG multiplier 

#stacked column (4 column array in this case)
flight_burn_data = np.column_stack((distance_lower_bound,
                                    distance_upper_bound,
                                    fuel_burn,
                                    passengers))

#create a dataframe from the column stack object
df = pd.DataFrame(flight_burn_data, columns=['distance(lower bound)', 
                                              'distance(upper bound)',
                                              'fuel burn',
                                              'passengers'])

##set range & step of distance data
distance_set = np.array(range(1000, 20000, 1000))

##list fuel burn results from distance_set 
fuel_burn_results = []
for var in distance_set:
    filter1 = df['distance(lower bound)']<=var
    filter2 = df['distance(upper bound)']>=var
    fburn_select = df['fuel burn'].where(filter1 & filter2, axis=0) 
    fburn_select = fburn_select.dropna()
    fburn_select = fburn_select.iloc[0]
    fuel_burn_results.append(fburn_select)

##list passenger results from distance_set
passenger_results = []
for var in distance_set:
    filter1 = df['distance(lower bound)']<=var
    filter2 = df['distance(upper bound)']>=var
    passenger_select = df['passengers'].where(filter1 & filter2, axis=0) 
    passenger_select = passenger_select.dropna()
    passenger_select = passenger_select.iloc[0]
    passenger_select = passenger_select * pass_load_factor
    passenger_results.append(passenger_select)

#create np.arrays
fuel_burn_results = np.array(fuel_burn_results)
passenger_results = np.array(passenger_results)

fburn_pass_selects = np.column_stack((distance_set,
                                      fuel_burn_results,
                                      passenger_results))

fbps = pd.DataFrame(fburn_pass_selects, columns=['distance data', 
                                                 'fuel burn results', 
                                                 'passenger results'])

#EMISSIONS CALCULATIONS
#calculate total fuel burnt 
fbps['fuel_burnt'] = fbps['distance data'] * fbps['fuel burn results']
fbps['pass_emissions'] = (fbps['fuel_burnt'] / fbps['passenger results']) * kg_co2_kg_fuel

#account for re-routing inefficiencies
fbps['pass_emissions'] = (fbps['pass_emissions'] * 0.1) + fbps['pass_emissions']

##add lifecycle cost of FUEL
fbps['fuel_lifecycle'] = (fbps['fuel_burnt'] * fuel_lifecycle) / fbps['passenger results']

#total emissions step 1
fbps['total emissions'] = fbps['fuel_lifecycle'] + fbps['pass_emissions']

#total emissions step 2 (GHG multiplier)
fbps['total emissions'] = fbps['total emissions'] *GHG_m


emissions_graph = fbps[['distance data','total emissions']]

graph = emissions_graph.plot.bar(x='distance data', rot=90, title='Carbon Calculator Outputs')
graph.set_xlabel("Distance (km)")
graph.set_ylabel("Total Emissions (kg CO2e)")

plt.show()
