#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 13:37:21 2019

@author: diwas
"""

######################### Import Necessary Library ################################
import fiona
from shapely.geometry import shape
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import shapefile
import pandas as pd
import numpy as np
import colour
from colour import Color
from shapely.geometry.polygon import LinearRing
#from matplotlib import pyplot
import matplotlib.pyplot as plt
#from matplotlib.patches import Polygon
import matplotlib
from descartes import PolygonPatch
import geopandas as gpd
from pandas import HDFStore, DataFrame
import time
############ Using Geo-Pandas for reading boundary shape files ################

start = time.time()

fp_NonSorted = gpd.read_file("...Path to the shape file /Boundary.shp") ## File should have the OBECTID for the objects in place ##
fp = fp_NonSorted.sort_values(by = ['OBJECTID'])
#fp_selected = fp.iloc[1:10,:]
fp_selected = fp.iloc[:,:]
fp_ID = fp_selected[['OBJECTID']]
fp_coord = fp_selected[['geometry']]

########## Using HDF5 reader for opening classified points #################

store = pd.HDFStore('... Ptah to classified data points /classified_points.h5')
points_csv = pd.read_hdf(store)
#points_coord = points_csv.iloc[:,1:5]
#working_points_NonSorted = points_csv.iloc[1:500,0:4] ## Use for Debugging ##
#working_points = working_points_NonSorted.sort_values(by=['boundary_id']) ## use for Debugging ##
working_points = points_csv.sort_values(by=['boundary_id']) ## for actual use ##


####################### Main Logic to check whether the points belong to the polygon ###########################

crop_id = [] ## crop id ##
crop_class = [] ## crop classified class ##
crop_class_weight = [] ## weighted percentage of the maximum occuring crop  ##
classified_polygon = [] ## Polygon ID ##

Farm_class = [] ## final crop_id assigned to the farm after max checking ##
Weighted_Percentage_of_Crop = [] ## percentage of crop maximum present in the farm ##
Crop_Name_on_Farm = [] ## Crop name assigned to farm based on its maximum occurence ##
Polygon_Color = [] ## color assigned to polgon just for visulization purpose ##

for i in range(1,len(fp_selected['OBJECTID'])):
    
    polygon_ID = fp_selected['OBJECTID'][i]
    
    for j in range(1,len(working_points['boundary_id'])):
        
    
        if (polygon_ID == working_points['boundary_id'][j]):
            
            crop_class.append(working_points['crop_id'][j])
            classified_polygon.append(polygon_ID)
            
            print('Done With {} polygon !!'.format(polygon_ID))
            
    Final_Classified_Lists = list(zip(crop_class,classified_polygon))
    Farm_Poly_Class = max(set(crop_class) , key = crop_class.count) ## Crop Class Assignment to a farm polygon ##
    
    Maximum_Class_Occurence = []
    for i in crop_class:
        if i == Farm_Poly_Class:
            Maximum_Class_Occurence.append(i)
        
        
#     print(len(heighst_class_len))
    max_poly_class_weight = (len(Maximum_Class_Occurence) / len(crop_class))*100
    
    if Farm_Poly_Class == 1:
        c = 'Bajra'
        color = '#ffe4e1'
    elif Farm_Poly_Class == 2:
        c = 'Okra'
        color = '#ae6634'
    elif Farm_Poly_Class == 3:
        c = 'Castor'
        color = '#b2c1ff'
    elif Farm_Poly_Class == 4:
        c = 'Gram'
        color = '#f3e165'
    elif Farm_Poly_Class == 5:
        c = 'Cotton'
        color = '#705800'
    elif Farm_Poly_Class == 6:
        c = 'Cumin'
        color = '#e67e22'
    elif Farm_Poly_Class == 7:
        c = 'Fennel'
        color = '#326983'
    elif Farm_Poly_Class == 8:
        c = 'Garlic'
        color = '#c6b6e0'
    elif Farm_Poly_Class == 9:
        c = 'Groundnut'
        color = '#40cad5'
    elif Farm_Poly_Class == 10:
        c = 'Gaur'
        color = '#ff11d0'
    elif Farm_Poly_Class == 11:
        c = 'Jowar'
        color = '#684dad'
    elif Farm_Poly_Class == 12:
        c = 'Maize'
        color = '#8af897'
    elif Farm_Poly_Class == 13:
        c = 'Onion'
        color = '#8aebf8'
    elif Farm_Poly_Class == 14:
        c = 'Rajko'
        color = '#ebf88a'
    elif Farm_Poly_Class == 15:
        c = 'Brinjal'
        color = '#f88aeb'
    elif Farm_Poly_Class == 16:
        c = 'Sava'
        color = '#75827d'
    elif Farm_Poly_Class == 17:
        c = 'Sesamum'
        color = '#4dd0e1'
    elif Farm_Poly_Class == 18:
        c = 'Sugarcane'
        color = '#003366'
    elif Farm_Poly_Class == 19:
        c = 'Sorghum'
        color = '#cccccc'
    elif Farm_Poly_Class == 20:
        c = 'Tur'
        color = '#daa520'
    elif Farm_Poly_Class == 21:
        c = 'Wheat'
        color = '#ffa500'
        
    else:
        color = '#ffdab9'
        
            
     
    Farm_class.append(Farm_Poly_Class)
    Weighted_Percentage_of_Crop.append(max_poly_class_weight)
    Crop_Name_on_Farm.append(c)
    Polygon_Color.append(color)
    print('Appending done for polygon Class {}'.format(Farm_Poly_Class))
    
    del crop_class[:] ## Reset every time after appending a set of crop classes for effective calculations ##
    
print("processing time: ", time.time() - start)        
    
############### (** OPTIONAL) Plotting the polygon with desired color (**Open Just for Visualization Purpose) #############33


for i in range(1,len(fp_selected['geometry'])):
    

    plotting_poly = Polygon(fp_selected['geometry'][i])
    plotting_color = Polygon_Color[i]

 
    plt.figure()
    axes = plt.gca()
    axes.add_patch(PolygonPatch(plotting_poly , facecolor = plotting_color))
    axes.axis('scaled')
    plt.show()
    print('Done_Plotting_with {} polygon'.format(i))


############### Open to save color and % weighted class to boundary shape file (FINAL STEP) #############################
    
filetosave = gpd.read_file('...Path to the shape file /Boundary.shp') ## save as reading boundary shape files ##
list_to_append_1 = Crop_Name_on_Farm
list_to_append_2 = Weighted_Percentage_of_Crop
list_to_append_3 = Polygon_Color
filetosave['crop_name'] = list_to_append_1
filetosave['color'] = list_to_append_3
filetosave['Maximum_Class_Weighted_Percentage'] = list_to_append_2
filetosave.to_file('... Path to directory to save appended atributes to shape file /Case_Final')
        
    
    
    
    
    
    
