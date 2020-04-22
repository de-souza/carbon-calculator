# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:56:06 2020

@author: agbon
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


##set range & step of distance data (BOTH DATASETS) #user-defined
range_min = 0
range_max = 20000
interval = 500 

distance_set = np.array(range(range_min, range_max, interval))

##START DATASET 1 INPUT##
distance_lower_bound = np.array([0, 801, 2001, 5501, 10001])
distance_upper_bound = np.array([800, 2000, 5500, 10000, 20000])    
fuel_burn = np.array([2.4, 3.42, 7.57, 7, 6.5])   
passengers = np.array([136, 180, 291, 350, 400])

pass_load_factor = 0.8 ##passenger load factor
kg_co2_kg_fuel = 3.15 #emissions per kg fuel burnt
inefficiencies = 0.1 #re-routing inefficiencies
fuel_lifecycle = 0.5064 #(kg CO2 / kg fuel)
GHG_m = 1.5 #GHG multiplier 

DS1 = str(' DS1')
##END DATASET 1 INPUT##


##START  DATASET 2 INPUT##
distance_lower_bound_2 = np.array([0, 801, 2001, 5501])
distance_upper_bound_2 = np.array([800, 2000, 5500, 20000])    
fuel_burn_2 = np.array([2.4, 3.42, 7.57, 6.29])   
passengers_2 = np.array([136, 180, 291, 572])

pass_load_factor_2 = 0.8 ##passenger load factor
kg_co2_kg_fuel_2 = 3.15 #emissions per kg fuel burnt
inefficiencies_2 = 0.1 #re-routing inefficiencies
fuel_lifecycle_2 = 0.5064 #(kg CO2 / kg fuel)
GHG_m_2 = 1.5 #GHG multiplier 

DS2 = str(' DS2')
##END DATASET 2 INPUT##



#stacked column (4 column array in this case)
flight_burn_data = np.column_stack((distance_lower_bound,
                                    distance_upper_bound,
                                    fuel_burn,
                                    passengers))

## stacked column (4 column array in this case)    #DS2#
flight_burn_data_2 = np.column_stack((distance_lower_bound_2,
                                    distance_upper_bound_2,
                                    fuel_burn_2,
                                    passengers_2))


#create a dataframe from the column stack object
df = pd.DataFrame(flight_burn_data, columns=['distance(lower bound)', 
                                              'distance(upper bound)',
                                              'fuel burn',
                                              'passengers'])


#create a dataframe from the column stack object #DS2#
df_2 = pd.DataFrame(flight_burn_data_2, columns=['distance(lower bound)', 
                                              'distance(upper bound)',
                                              'fuel burn',
                                              'passengers'])



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

##list fuel burn results from distance_set  #DS2#
fuel_burn_results_2 = []
for var in distance_set:
    filter1 = df_2['distance(lower bound)']<=var
    filter2 = df_2['distance(upper bound)']>=var
    fburn_select_2 = df_2['fuel burn'].where(filter1 & filter2, axis=0) 
    fburn_select_2 = fburn_select_2.dropna()
    fburn_select_2 = fburn_select_2.iloc[0]
    fuel_burn_results_2.append(fburn_select_2)

##list passenger results from distance_set #DS2#
passenger_results_2 = []
for var in distance_set:
    filter1 = df_2['distance(lower bound)']<=var
    filter2 = df_2['distance(upper bound)']>=var
    passenger_select_2 = df_2['passengers'].where(filter1 & filter2, axis=0) 
    passenger_select_2 = passenger_select_2.dropna()
    passenger_select_2 = passenger_select_2.iloc[0]
    passenger_select_2 = passenger_select_2 * pass_load_factor_2
    passenger_results_2.append(passenger_select_2)



#create np.arrays
fuel_burn_results = np.array(fuel_burn_results)
passenger_results = np.array(passenger_results)

fburn_pass_selects = np.column_stack((distance_set,
                                      fuel_burn_results,
                                      passenger_results))


#create np.arrays #DS2#
fuel_burn_results_2 = np.array(fuel_burn_results_2)
passenger_results_2 = np.array(passenger_results_2)

fburn_pass_selects_2 = np.column_stack((distance_set,
                                      fuel_burn_results_2,
                                      passenger_results_2))



#fbps = dataframe of fuel burn and passenger data
fbps = pd.DataFrame(fburn_pass_selects, columns=['distance data', 
                                                 'fuel burn results', 
                                                 'passenger results'])


#fbps2 = dataframe of fuel burn and passenger data #DS2#
fbps_2 = pd.DataFrame(fburn_pass_selects_2, columns=['distance data', 
                                                 'fuel burn results', 
                                                 'passenger results'])



#define emissions calculation function
def emissions_calc(dataframe):
    #calculate total fuel burnt 
    dataframe['fuel_burnt'] = dataframe['distance data'] * dataframe['fuel burn results']
    dataframe['pass_emissions'] = (dataframe['fuel_burnt'] / dataframe['passenger results']) * kg_co2_kg_fuel
    #account for re-routing inefficiencies
    dataframe['pass_emissions'] = (dataframe['pass_emissions'] * 0.1) + dataframe['pass_emissions']
    ##add lifecycle cost of FUEL
    dataframe['fuel_lifecycle'] = (dataframe['fuel_burnt'] * fuel_lifecycle) / dataframe['passenger results']
    #total emissions step 1
    dataframe['total emissions'] = dataframe['fuel_lifecycle'] + dataframe['pass_emissions']
    #total emissions step 2 (GHG multiplier)
    dataframe['total emissions'] = dataframe['total emissions'] *GHG_m

    return dataframe

#EMISSIONS CALCULATIONS #DS1#
fbps = emissions_calc(fbps)

##EMISSIONS CALCULATIONS #DS2#
fbps_2 = emissions_calc(fbps_2)

##END EMISSIONS CALCULATIONS##

emissions_graph = fbps[['distance data','total emissions']]     #DS1

emissions_graph_2 = fbps_2[['distance data','total emissions']]  #DS2


#additional analysis #DS1
fbps['% change'] = fbps['total emissions'].pct_change()
emissions_graph2 = fbps[['distance data', '% change']]

#additional analysis #DS2
fbps_2['% change'] = fbps_2['total emissions'].pct_change()
emissions_graph2_2 = fbps_2[['distance data', '% change']]




#using matplotlib
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12.5,8), dpi=250)
plt.style.use('default')

#graphs organized by axis
x1 = emissions_graph['distance data']
y1 = emissions_graph['total emissions']


ax[0,0].plot(x1, y1, color='g')
ax[0,0].set_title(('Emission Calculator Output' +str(DS1)), fontsize=12, fontweight='bold')
ax[0,0].set_ylabel('kg CO2e')
ax[0,0].set_xlabel('distance (km)')
ax[0,0].set_xticklabels(x1, rotation=45, fontsize=7) #x tick labels
ax[0,0].set_yticklabels(y1, fontsize=7)
ax[0,0].yaxis.set_major_formatter(FormatStrFormatter('%i'))
ax[0,0].xaxis.set_major_formatter(FormatStrFormatter('%i'))
ax[0,0].set_yticks(range(0,2400,250))
ax[0,0].set_ylim([0,2400])
ax[0,0].set_xticks(range(range_min,range_max,1000))
ax[0,0].set_xlim([range_min,range_max])
                                  
x2 = emissions_graph2['distance data']
y2 = emissions_graph2['% change']

ax[0,1].plot(x2, y2)
ax[0,1].set_title(('% change from last distance' +str(DS1)), fontsize=12, fontweight='bold')
ax[0,1].set_ylabel('% change')
ax[0,1].set_xlabel('distance (km)')
ax[0,1].set_xticklabels(x1, rotation=45, fontsize=7)
ax[0,1].set_yticklabels(y1, fontsize=7)
ax[0,1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax[0,1].xaxis.set_major_formatter(FormatStrFormatter('%i'))
ax[0,1].set_ylim([-0.5,3])
ax[0,1].set_xticks(range(range_min,range_max,1000))
ax[0,1].set_xlim([range_min,range_max])

# plt.subplots_adjust(wspace=0.5, hspace=0.7)

#DS2 graphing 
x1_2 = emissions_graph_2['distance data']
y1_2 = emissions_graph_2['total emissions']


ax[1,0].plot(x1_2, y1_2, color='g')
ax[1,0].set_title(('Emission Calculator Output' +str(DS2)), fontsize=12, fontweight='bold')
ax[1,0].set_ylabel('kg CO2e')
ax[1,0].set_xlabel('distance (km)')
ax[1,0].set_xticklabels(x1, rotation=45, fontsize=7) #x tick labels
ax[1,0].set_yticklabels(y1, fontsize=7)
ax[1,0].yaxis.set_major_formatter(FormatStrFormatter('%i'))
ax[1,0].xaxis.set_major_formatter(FormatStrFormatter('%i'))
ax[1,0].set_yticks(range(0,2400,250))
ax[1,0].set_ylim([0,2400])
ax[1,0].set_xticks(range(range_min,range_max,1000))
ax[1,0].set_xlim([range_min,range_max])
                                  
x2_2 = emissions_graph2_2['distance data']
y2_2 = emissions_graph2_2['% change']

ax[1,1].plot(x2_2, y2_2)
ax[1,1].set_title(('% change from last distance' +str(DS2)), fontsize=12, fontweight='bold')
ax[1,1].set_ylabel('% change')
ax[1,1].set_xlabel('distance (km)')
ax[1,1].set_xticklabels(x1, rotation=45, fontsize=7)
ax[1,1].set_yticklabels(y1, fontsize=7)
ax[1,1].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
ax[1,1].xaxis.set_major_formatter(FormatStrFormatter('%i'))
ax[1,1].set_ylim([-0.5,3])
ax[1,1].set_xticks(range(range_min,range_max,1000))
ax[1,1].set_xlim([range_min,range_max])

plt.subplots_adjust(wspace=0.25, hspace=0.45)









