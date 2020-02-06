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
# This script takes as inputs, 
# 1) an XML file of data downloaded
# from the National Transportation Safety Board's database of 
# aviation accidents.
# (http://www.ntsb.gov/_layouts/ntsb.aviation/index.aspx)
# 2) Data in .json format from the incident narratives
#
# Processes includes:
#  A) loading datasets into pandas dataframes
#  B) creating a case-study dataset of just Non-US, Non- Commercial
#   flights, and comparing them to the full data set
#  C) Adding context with text analysis 
#
# 
############################################################
#### SUMMARY FINDINGS 
############################################################
#
# FAR Description
# A really interesting finding from the EDA was  that 76% of accidents 
# that occur for Non-U.S., Non-Commercial flights lead to a fatality 
#(512 of 677).This is a really massive majority, making it a topic of 
# keen interest to explore in the text data. It makes me curious if 
# there are factors that could be modified or improved to prevent 
# these accidents from having such fatal outcomes.


# What is a FAR Description?

# From the data dictionary- Federal Aviation Reg. Part
#The applicable regulation part (14 CFR) or authority the aircraft was 
#operating under at the time of the accident. Further research on the
# FAR website (https://www.ecfr.gov/cgi-bin/text-idx?c=ecfr&tpl=/ecfrbrowse/Title14/14tab_02.tpl)
# shows the categorization of the category of air transportation vehicle
#  is extremely complicated. Factors that influence designation in addition
# to the obvious ones (military, space craft, etc), include if the flight
# is a regular transportation carrier, charter vehicle, as well as where the
# pilot and crew are from/ certified.
#
# In a real-life project, this would be the point in the project when I would
# want to speak with a subject matter expert to gain insight into what kind of
# flights this designation describes.

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
### Convert JSON data from single file to pandas DataFrame
###########################################################

#load json file to object
with open('./data/NarrativeData_499.json') as f:
  data = json.load(f)
  
#function to extract json values and create field lists
def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

#field lists for each set of json values
Event_ID = extract_values(data, 'EventId')
narrative = extract_values(data, 'narrative')
cause = extract_values(data, 'probable_cause')

#combine lists into a pandas dataframe
json_df = pd.DataFrame(list(zip(Event_ID,narrative,cause)), columns= ["Event_ID", "Narrative", "Cause"])

###########################################################
### Data Cleaning
###########################################################
#
xml_df.dtypes

print(len(xml_df[xml_df["InvestigationType"]=='Incident']))
# 3050 incidents

## CAUTION!!!!!
## CAUTION!!!!!
## CAUTION!!!!! 
## Assumption made here that a missing value is 0, would 
## want to confirm by cross referencing with narratives. (if time)


# Turn blanks to 0 for fatalities, make int
xml_df['TotalFatalInjuries'] = xml_df['TotalFatalInjuries'].replace({'':'0'})
xml_df['TotalFatalInjuries'] = xml_df['TotalFatalInjuries'].astype(int)

# Turn blanks to 0 for serious injuries, make int
xml_df['TotalSeriousInjuries'] = xml_df['TotalSeriousInjuries'].replace({'':'0'})
xml_df['TotalSeriousInjuries'] = xml_df['TotalSeriousInjuries'].astype(int)

# Turn blanks to 0 for minor injuries, make int
xml_df['TotalMinorInjuries'] = xml_df['TotalMinorInjuries'].replace({'':'0'})
xml_df['TotalMinorInjuries'] = xml_df['TotalMinorInjuries'].astype(int)

# Turn blanks to 0 for unijured, make int
xml_df['TotalUninjured'] = xml_df['TotalUninjured'].replace({'':'0'})
xml_df['TotalUninjured'] = xml_df['TotalUninjured'].astype(int)

col = list(xml_df.columns)
print(col)
['EventId', 'InvestigationType', 'AccidentNumber', 'EventDate', 'Location', 
 'Country', 'Latitude', 'Longitude', 'AirportCode', 'AirportName', 
 'InjurySeverity', 'AircraftDamage', 'AircraftCategory', 'RegistrationNumber', 
 'Make', 'Model', 'AmateurBuilt', 'NumberOfEngines', 'EngineType', 
 'FARDescription', 'Schedule', 'PurposeOfFlight', 'AirCarrier', 
 'TotalFatalInjuries', 'TotalSeriousInjuries', 'TotalMinorInjuries', 
 'TotalUninjured', 'WeatherCondition', 'BroadPhaseOfFlight', 'ReportStatus', 
 'PublicationDate']

###########################################################
### Quantifying this population in context
###########################################################
# 7420 Accidents
# 
# .007 % of accidents
# 

accidents = xml_df[xml_df["InvestigationType"]=="Accident"] #7420 Accidents
nuncf = xml_df[xml_df["FARDescription"]=="Non-U.S., Non-Commercial"] #667
## 9% of Accidents are from this group

print(accidents["TotalFatalInjuries"].sum()) #43995
print(nuncf["TotalFatalInjuries"].sum()) #1284
## 3% of fatalities

print(len(accidents[accidents["TotalFatalInjuries"]>0])) #15409
print(len(nuncf[nuncf["TotalFatalInjuries"]>0])) #512
## 3% of crashes

## But 77% are fatal!

## lets look at this group a little more

stats = nuncf.describe()
for i in stats:
    print(stats[i])
'''
count    677.000000
mean       1.896603
std        2.134100
min        0.000000
25%        1.000000
50%        1.000000
75%        3.000000
max       26.000000
Name: TotalFatalInjuries, dtype: float64
count    677.000000
mean       0.254062
std        0.686192
min        0.000000
25%        0.000000
50%        0.000000
75%        0.000000
max        5.000000
Name: TotalSeriousInjuries, dtype: float64
count    677.000000
mean       0.184638
std        0.892043
min        0.000000
25%        0.000000
50%        0.000000
75%        0.000000
max       10.000000
Name: TotalMinorInjuries, dtype: float64
count    677.000000
mean       0.765140
std        7.910713
min        0.000000
25%        0.000000
50%        0.000000
75%        0.000000
max      203.000000
Name: TotalUninjured, dtype: float64
'''

# and compare to the whole
stats = xml_df.describe()
for i in stats:
    print(stats[i])
 '''   
    count    77257.000000
mean         0.569748
std          5.185111
min          0.000000
25%          0.000000
50%          0.000000
75%          0.000000
max        349.000000
Name: TotalFatalInjuries, dtype: float64
count    77257.000000
mean         0.215579
std          1.150267
min          0.000000
25%          0.000000
50%          0.000000
75%          0.000000
max        111.000000
Name: TotalSeriousInjuries, dtype: float64
count    77257.000000
mean         0.348952
std          2.350439
min          0.000000
25%          0.000000
50%          0.000000
75%          0.000000
max        380.000000
Name: TotalMinorInjuries, dtype: float64
count    77257.000000
mean         4.873617
std         26.900906
min          0.000000
25%          0.000000
50%          1.000000
75%          2.000000
max        699.000000
Name: TotalUninjured, dtype: float64
'''


#xml_df mean fatalities       0.215579
#nuncf mean fatalities        0.254062

#xm;_df mean serious inj      0.348952
#nuncf mean serious inj       0.184638

print(xml_df["AircraftCategory"].describe())
print(nuncf["AircraftCategory"].describe())


count     77257
unique       13
top            
freq      60737
Name: AircraftCategory, dtype: object
count          677
unique           4
top       Airplane
freq           434
Name: AircraftCategory, dtype: object

print(nuncf["AircraftCategory"].unique())
#['Helicopter' 'Airplane' '' 'Balloon']

print(nuncf[nuncf["AircraftCategory"]=="Helicopter"].sum())
print(len(nuncf[nuncf["AircraftCategory"]=="Helicopter"])) #153

#TotalFatalInjuries                                271
#TotalSeriousInjuries                               44
#TotalMinorInjuries                                 47
#TotalUninjured                                     81

#61% of passengers in accidents died 271/443 passengers


print(nuncf[nuncf["AircraftCategory"]=="Airplane"].sum())
print(len(nuncf[nuncf["AircraftCategory"]=="Airplane"])) #434

#TotalFatalInjuries                               842
#TotalSeriousInjuries                             120
#TotalMinorInjuries                                66
#TotalUninjured                                   393                                                47

# 59% of airline accicents were fatal       842/1421 passengers


# Okay, so let's look at Non-US, Non-Commercial Helicopter Accidents


nuncf_heli = nuncf[nuncf["AircraftCategory"]=="Helicopter"]

nuncf_heli = nuncf_heli[nuncf_heli["InvestigationType"]=="Accident"]
#Now we are looking at 150 records for this population

for i in col:
    print(nuncf_heli[i].describe())
'''
count                150
unique               150
top       20110414X33613
freq                   1
Name: EventId, dtype: object

count                   150
unique                  148
top       Sao Paulo, Brazil
freq                      2


Name: Location, dtype: object
count        150
unique        49
top       Brazil
freq          20
Name: Country, dtype: object
--May be interesting to map these
'''

print(print(nuncf_heli["Country"].unique()))
'''
['Paraguay' 'Russia' 'Brazil' 'Turkey' 'Chile' 'Sweden' 'Portugal'
 'Dominican Republic' 'Venezuela' 'Colombia' 'Belgium' 'France'
 'United Kingdom' 'Germany' 'Kazakhstan' 'Argentina' 'Poland' 'India'
 'Trinidad And Tobago' 'Australia' 'New Zealand' 'Bangladesh' 'Finland'
 'Bahamas' 'Guatemala' 'Mexico' 'Malaysia' 'Latvia' 'China' 'Spain'
 'Ecuador' 'Vanuatu' 'Canada' 'United States' 'Papua New Guinea' 'Italy'
 'Peru' 'Costa Rica' 'Belarus' 'Uruguay' 'Philippines' 'Israel'
 'South Africa' 'Ireland' 'Netherlands Antilles' 'Panama' 'Hungary'
 'Haiti' 'Greece']
'''

print(nuncf_heli[nuncf_heli["TotalFatalInjuries"]>0].groupby('Country')["TotalFatalInjuries"].count().sort_values(ascending=False))
print(nuncf_heli.groupby('Country')["TotalFatalInjuries"].count().sort_values(ascending=False))
print(nuncf_heli.groupby('Country')["EventId"].count().sort_values(ascending=False))

'''
Country   Fatal_Accidents   Fatalities    Accidents    % Fatal
Brazil                19    20             20              95%
Australia             10    12             12              83%
Russia                 9    12             12              75%
Germany                6    7              7               86%
Colombia               6    7              7               86%
United Kingdom         5    7              7               71%
Venezuela              4    6              6               67%
Spain                  4    4              4              100%
France                 4    4              4              100%
Malaysia               3    3              3              100%
Mexico                 3    8              8               38%
Chile                  3    5              5               60%
Italy                  3    3              3              100%
Haiti                  2
India                  2    
Canada                 2
Ireland                2
Argentina              2
Paraguay               2
South Africa           2
Vanuatu                1
China                  1
Uruguay                1
Bahamas                1
Belarus                1
Belgium                1
United States          1
Portugal               1
Poland                 1
Kazakhstan             1
Dominican Republic     1
Philippines            1
Guatemala              1
Panama                 1
Hungary                1
New Zealand            1
Israel                 1
'''

## Well, Brazil is certainly fascinating! 
# I wonder if they have something regularly going on with 
# helicopters in the US. 

brazil_heli= nuncf_heli[nuncf_heli["Country"]=="Brazil"]

print(brazil_heli["Make"].unique())

['BELL' 'ROBINSON' 'AGUSTA' 'EMBRAER']









################# Extra Exploration #####################
print(nuncf_heli["Make"].unique())


'''
['ROBINSON' 'BELL' 'HUGHES' 'SCHWEIZER' 'ROBINSON HELICOPTER'
 'ROBINSON HELICOPTER COMPANY' 'EUROCOPTER' 'ENSTROM' 'MD HELICOPTER'
 'AGUSTA' 'AEROSPATIALE' 'MCDONNELL DOUGLAS' '' 'SIKORSKY'
 'McDonnell Douglas Helicopter' 'Scotts-Bell 47, Inc.'
 'BELL HELICOPTER TEXTRON CANADA' 'ERICKSON' 'BOLKOW' 'EMBRAER' 'Robinson'
 'Eurocopter Deutsch' 'Schweizer' 'Bell' 'Garlick' 'Eurocopter' 'Mil']
'''
print(nuncf_heli[nuncf_heli["TotalFatalInjuries"]>0].groupby('Make')["TotalFatalInjuries"].count().sort_values(ascending=False))
print(nuncf_heli.groupby('Make')["TotalFatalInjuries"].count().sort_values(ascending=False))
print(nuncf_heli.groupby('Make')["EventId"].count().sort_values(ascending=False))

'''
Fatal Accidents by Make
ROBINSON                          45
BELL                              25
Robinson                           5
HUGHES                             5
EUROCOPTER                         4
SCHWEIZER                          3
AGUSTA                             3
ENSTROM                            2
ROBINSON HELICOPTER COMPANY        2
AEROSPATIALE                       2
BELL HELICOPTER TEXTRON CANADA     1
BOLKOW                             1
Bell                               1

Fatalities by Make
ROBINSON                          53
BELL                              36
Bell                               9
HUGHES                             7
EUROCOPTER                         7
Robinson                           6
AGUSTA                             3
MCDONNELL DOUGLAS                  3
SCHWEIZER                          3
AEROSPATIALE                       3
ROBINSON HELICOPTER COMPANY        2
ENSTROM                            2
                                   2
ERICKSON                           1
BELL HELICOPTER TEXTRON CANADA     1

Accidents by Make (All Countries)
ROBINSON                          53
BELL                              36
Bell                               9
HUGHES                             7
EUROCOPTER                         7
Robinson                           6
AGUSTA                             3


'''

count          150
unique          27
top       ROBINSON
freq            53
Name: Make, dtype: object








count     150
unique     64
top       R44
freq       29
Name: Model, dtype: object
count     150
unique      3
top        No
freq      138
Name: AmateurBuilt, dtype: object
count     150
unique      3
top         1
freq       76
Name: NumberOfEngines, dtype: object
count     150
unique      5
top          
freq       86
Name: EngineType, dtype: object
count                          150
unique                           1
top       Non-U.S., Non-Commercial
freq                           150
Name: FARDescription, dtype: object
count     150
unique      3
top          
freq      143
Name: Schedule, dtype: object
count         150
unique         16
top       Unknown
freq           60
Name: PurposeOfFlight, dtype: object
count     150
unique      1
top          
freq      150
Name: AirCarrier, dtype: object
count    150.000000
mean       1.806667
std        2.100485
min        0.000000
25%        0.000000
50%        1.000000
75%        2.000000
max       13.000000
Name: TotalFatalInjuries, dtype: float64
count    150.000000
mean       0.293333
std        0.798881
min        0.000000
25%        0.000000
50%        0.000000
75%        0.000000
max        4.000000
Name: TotalSeriousInjuries, dtype: float64
count    150.000000
mean       0.313333
std        1.193588
min        0.000000
25%        0.000000
50%        0.000000
75%        0.000000
max       10.000000
Name: TotalMinorInjuries, dtype: float64
count    150.000000
mean       0.533333
std        1.863340
min        0.000000
25%        0.000000
50%        0.000000
75%        0.000000
max       18.000000
Name: TotalUninjured, dtype: float64
count     150
unique      4
top          
freq       80
Name: WeatherCondition, dtype: object
count     150
unique      5
top          
freq      141
Name: BroadPhaseOfFlight, dtype: object
count         150
unique          2
top       Foreign
freq          149
Name: ReportStatus, dtype: object
count     150
unique    107
top          
freq       38
Name: PublicationDate, dtype: object
'''