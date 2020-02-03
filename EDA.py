#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPLORATORY DATA ANALYSIS
RTI Exercise #2

Created on Sun Feb  2 20:29:27 2020

@author: allisonyoung
"""



## Import Files
import json
import pandas as pd
import xml.etree.ElementTree as et


##########################################################
### Convert XML Data file to pandas DataFrame
##########################################################

## label file path
path_to_xml_file = "./Data/AviationData.xml"

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
with open('./Data/NarrativeData_499.json') as f:
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
### EDA of XML DataFrame
###########################################################

stats = xml_df.describe()
for i in stats:
    print(stats[i])
    
###########################################################
### Identifiers
###########################################################
    

##### Unique Flight Idetifier: EventID ######################
'''
count              77257
unique             76133
top       20101022X34140
freq                   3
Name: EventId, dtype: object
'''
##### Unique Accident Idetifier: AccidentNumber ############
'''
count          77257
unique         77257
top       LAX90LA318
freq               1
Name: AccidentNumber, dtype: object
'''
##### Unique Registration Idetifier: RegistrationNumber ######################
'''
count     77257
unique    67493
top            
freq       2756
Name: RegistrationNumber, dtype: object
'''
#TODO: Calculate percent accidents (98.5% of incidents are accidents)

###########################################################
### Outcome Variables
###########################################################

##### Continuous Variables (5) ############################
# Total Fatal Injuries
# Total Serious Injuries
# Total Minor Injuries
# Total Uninjured
# TODO: ---add together for total passengers?
''''
    
#count     77257
#unique      118
#top           0
#freq      40363
#Name: TotalFatalInjuries, dtype: object

count     77257
unique       41
top           0
freq      42955
Name: TotalSeriousInjuries, dtype: object

count     77257
unique       63
top           0
freq      40342
Name: TotalMinorInjuries, dtype: object

count     77257
unique      364
top           1
freq      22029
Name: TotalUninjured, dtype: object

'''
##### Categorical Variables () ##############################
# Injury Severity
# Aircraft Damage

'''
count         77257
unique          120
top       Non-Fatal
freq          58499
Name: InjurySeverity, dtype: object

count           77257
unique              4
top       Substantial
freq            55420
Name: AircraftDamage, dtype: object
'''

###########################################################
### Predictor Variables
###########################################################


##### Continuous Variables (5) ############################
# Number of Engines
'''
#count     77257
#unique        8
#top           1
#freq      61465
#Name: NumberOfEngines, dtype: object
'''

##### Boolean Variables (1) ################################
# Amateur Built
# TODO: Add any customized booleans [ie- any injuries, any fatalities, etc]
'''
count     77257
unique        3
top          No
freq      69198
Name: AmateurBuilt, dtype: object

'''
##### Date Variables (2) ##############################
# Event Date
# TODO: convert Publication Date to date field

'''
count          77257
unique         12180
top       06/30/1984
freq              25
Name: EventDate, dtype: object

count     77257
unique     3403
top            
freq      13188
Name: PublicationDate, dtype: object
'''

##### Text Variables (2) ######################################
# Location
# Airport Name

'''
count             77257
unique            24702
top       ANCHORAGE, AK
freq                372
Name: Location, dtype: object

count     77257
unique    22284
top            
freq      29926
Name: AirportName, dtype: object
'''
##### Categorical Variables (13) ##############################
# InvestigationType
# Airport Code
# Aircraft Category
# Make
# Model
# EngineType
# FAR Description
# Schedule
# Purpose of Flight
# AirCarrier
# Weather Condition
# Broad Phase of Flight
# Probable Cause
'''

count        77257
unique           2
top       Accident
freq         74207
Name: InvestigationType, dtype: object

count     77257
unique     9489
top            
freq      33780
Name: AirportCode, dtype: object

count     77257
unique       13
top            
freq      60737
Name: AircraftCategory, dtype: object

count      77257
unique      7204
top       CESSNA
freq       16609
Name: Make, dtype: object

count     77257
unique    11029
top         152
freq       2251
Name: Model, dtype: object

count             77257
unique               15
top       Reciprocating
freq              63016
Name: EngineType, dtype: object

count     77257
unique       17
top            
freq      60592
Name: FARDescription, dtype: object

count     77257
unique        4
top            
freq      65878
Name: Schedule, dtype: object

count        77257
unique          23
top       Personal
freq         43360
Name: PurposeOfFlight, dtype: object

count     77257
unique     2814
top            
freq      73439
Name: AirCarrier, dtype: object

count     77257
unique        4
top         VMC
freq      68764
Name: WeatherCondition, dtype: object

count       77257
unique         13
top       LANDING
freq        18553
Name: BroadPhaseOfFlight, dtype: object

count              77257
unique                 4
top       Probable Cause
freq               72264
Name: ReportStatus, dtype: object

'''


##### Geospatial Variables (3)###########################
# Country
# Latitude
# Longitude
# TODO: convert lat and long to geopandas

'''
count             77257
unique              174
top       United States
freq              73076
Name: Country, dtype: object

count     77257
unique    16343
top            
freq      53496
Name: Latitude, dtype: object

count     77257
unique    17471
top            
freq      53505
Name: Longitude, dtype: object
'''

