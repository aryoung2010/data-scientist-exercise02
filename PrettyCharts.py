#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case Study on Non-US, Non-Commercial Flight Fatalities

Created on Wed Feb  5 19:46:24 2020

@author: allisonyoung
"""
############################################################
#### File Summary ##########################################
############################################################
#
# This script takes as inputs:
#1) an XML file of data downloaded
#from the National Transportation Safety Board's database of 
#aviation accidents.
#(http://www.ntsb.gov/_layouts/ntsb.aviation/index.aspx)
#
#***** If time, text analysis output 
#
#A) loading dataset into pandas dataframes
#B) creating a bar chart to illustrate interst in the Non-US, 
#Non- Commercial flights, as compared to other groups
#C) Map of countries with fatal helicopter crashes by fatalities
#in non-us, non-commercial group

#***** if time: D) Word cloud of relevant text from narrative exploration

#Additional Visualizations created outside of python 
#for summary document include:
#E)Calculations of helicopter vs airplane fatalities in these groups
#F( Table of high frequency makes and models for brazilian helicopter accidents, 
#with helicopter graphic descriptions
# 
############################################################
#### SUMMARY FINDINGS 
############################################################
#
# Brazillian helicopter accidents resulted in 43 deaths and 
# 19 of the 20 accidents were fatal (95%). Essentially, if a Brazilian
# helicopter goes down, it is bad news for the passengers and they are not 
# likely to survive. 13 of the 20 accidents were aboard Robinson helicopters,
# and more than half of those (8) were the R44 model.
#

##########################################################
#### CODE ################################################
##########################################################
## Import Files
import json
import pandas as pd
import xml.etree.ElementTree as et
import numpy as np
import seaborn as sns #visualisation
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from urllib.request import urlopen
import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objs as gobj
#chart_studio.tools.set_credentials_file(username='', api_key='')
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)


pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)


##########################################################
### Convert XML Data file to pandas DataFrame
##########################################################

## label file path
path_to_xml_file = "./data/AviationData.xml"

# Load xml file data
tree = et.parse(path_to_xml_file)
data = []
for el in tree.iterfind('./*'):
    for i in el.iterfind('*'):
        data.append(dict(i.items()))

##create pandas dataframe to hold data
xml_df = pd.DataFrame(data)


###########################################################
### Data Cleaning
###########################################################
#

## CAUTION!!!!!
## CAUTION!!!!!
## CAUTION!!!!! 
## Assumption made here that a missing value is 0, would 
## want to confirm by cross referencing with narratives. (if time)


# Turn blanks to 0 for fatalities, make int
xml_df['TotalFatalInjuries'] = xml_df['TotalFatalInjuries'].replace({'':'0'})
xml_df['TotalFatalInjuries'] = xml_df['TotalFatalInjuries'].astype(int)


###########################################################
### FARD CHART
###########################################################


xml_df["Fatality_bin"] = np.nan
xml_df['Fatality_bin'].loc[xml_df['InjurySeverity'].str.contains("Fatal\(")==False] = "Non-Fatal"
xml_df['Fatality_bin'].loc[xml_df['InjurySeverity'].str.contains("Fatal\(")==True] = "Fatal"

xml_df["Fatality_bin"].head(15)
mod_df =xml_df[xml_df["Fatality_bin"].notnull()]

xml_df = xml_df[xml_df["InvestigationType"]=="Accident"] #7420 Accidents
nuncf = xml_df[xml_df["FARDescription"]=="Non-U.S., Non-Commercial"] #667
## 9% of Accidents are from this group


fatal_mod = pd.DataFrame(mod_df[mod_df["Fatality_bin"]=="Fatal"].groupby("FARDescription")['Fatality_bin'].count())
nonfatal_mod = pd.DataFrame(mod_df[mod_df["Fatality_bin"]=="Non-Fatal"].groupby("FARDescription")['Fatality_bin'].count())
per_fatal = fatal_mod/(fatal_mod+nonfatal_mod)

print(per_fatal)

per_fatal = per_fatal.sort_values(by="Fatality_bin", ascending=False).reset_index()

per_fatal = per_fatal.dropna()

fard =sns.catplot("Fatality_bin", "FARDescription", kind="bar", data=per_fatal)


plt.title("Percent of Accidents resulting in Fatalities, by FAR Description")
plt.xlabel("Number of Fatal Accidents")
plt.ylabel("FAR Description")
plt.xlim(0, 1)

fard.savefig("FARD_chart.png")


############################################################
###
############################################################
brazil_heli= nuncf_heli[nuncf_heli["Country"]=="Brazil"]

nuncf_heli = nuncf[nuncf["AircraftCategory"]=="Helicopter"]

print(brazil_heli.groupby(['Make','Model'])["TotalFatalInjuries"].count().sort_values(ascending=False))

###########################################################
### NON-US, NON-COMMERCIAL HELICOPTER ACCIDENTS BY COUNTRY
###########################################################

#
#
#
#
#

nuncf_heli = nuncf[nuncf["AircraftCategory"]=="Helicopter"]

fatal_heli = pd.DataFrame(nuncf_heli[nuncf_heli["Fatality_bin"]=="Fatal"].groupby('Country')["Fatality_bin"].count().sort_values(ascending=False))
nonfatal_heli = pd.DataFrame(nuncf_heli[nuncf_heli["Fatality_bin"]=="Non-Fatal"].groupby('Country')["Fatality_bin"].count().sort_values(ascending=False))
perfatal_heli = fatal_heli/(fatal_heli+nonfatal_heli)

perfatal_heli= perfatal_heli.sort_values(by="Fatality_bin", ascending=False).reset_index()

perfatal_heli = perfatal_heli.dropna()


data = dict(type = 'choropleth',
            locations = perfatal_heli['Country'],
            locationmode = 'country names',
            autocolorscale = False,
            colorscale = 'blues',
            text= perfatal_heli['Country'],
            z= perfatal_heli["Fatality_bin"],
            marker = dict(line = dict(color = 'rgb(255,255,255)',width = 1)),
            colorbar = {'title':'Colour Range','len':0.25,'lenmode':'fraction'})
layout = dict(geo = dict(scope='world'))
worldmap = gobj.Figure(data = [data],layout = layout)

worldmap.update_layout(
    title="Non-US, Non-Commercial Countries with the Highest <br> Percentage of Fatal Helicopter Accidents",
    xaxis_title="x Axis Title",
    yaxis_title="y Axis Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)
plot(worldmap)
#py.iplot(worldmap, filename='Countries with High Percentage of Fatal Accidents')


