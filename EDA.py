#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXPLORATORY DATA ANALYSIS
RTI Exercise #2

Created on Sun Feb  2 20:29:27 2020

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
# EDA Process includes:
#  loading datasets into pandas dataframes
#  exploring both outcome and predictor variables 
#
# 

############################################################
#### SUMMARY FINDINGS 
############################################################
#
## Accidents
# 77275 records (74207 Accidents (96%), 3050 incidents (4%))
#
# 97% of incidents + accidents resulted in aircraft damage
# no incidents resulted in injuries
# 21 % of accidents were fatal, whereas 79% were non-fatal
#
## Fatalities
# most accidents fewer than 30
# outliers at 349, (>300)
# (second set between 175-300, third tier about 30-174)
#
## Serious Injuries
# most accidents fewer than 10 serious injuries
# outliers above 100 (two)-- three >80
# (second set between 30 and 85,  third tier about 11-29)
#
#

#### QUESTIONS ############################################
#
# What is a flight identifier vs record idenentifier?
#
#


#### NEXT STEPS ###########################################
#
#  1) Create Outcome variables to model/look at predictors
#  2) Compare predictor variables to outcomes
# (check for colinearity across plane variables)
#  3) Attempt a linear or logistic model
#  (if time)
#  4) Map geolocations of accidents
#  
# Text Data
#  1) create corpus
#  2) remove stop words
#  3) basic topic analysis 
#  4) assess added value to quantitative data
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
import matplotlib.pyplot as plt #visualisation
sns.set(color_codes=True)


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
### Data Cleaning
###########################################################
#
xml_df.dtypes

## CAUTION!!!!!
## CAUTION!!!!! Assumption made here that a missing value is null 
## CAUTION!!!!!

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



###########################################################
### EDA of XML DataFrame
###########################################################

stats = xml_df.describe()
for i in stats:
    print(stats[i])

#print(xml_df.isnull().sum()) # no missing values?
#print(xml_df == '').sum(axis=0) # no blank values?....doesnt seem right
num_records = len(xml_df)

print(xml_df.columns)
col = list(xml_df.columns)
'''
Index(['EventId', 'InvestigationType', 'AccidentNumber', 'EventDate',
       'Location', 'Country', 'Latitude', 'Longitude', 'AirportCode',
       'AirportName', 'InjurySeverity', 'AircraftDamage', 'AircraftCategory',
       'RegistrationNumber', 'Make', 'Model', 'AmateurBuilt',
       'NumberOfEngines', 'EngineType', 'FARDescription', 'Schedule',
       'PurposeOfFlight', 'AirCarrier', 'TotalFatalInjuries',
       'TotalSeriousInjuries', 'TotalMinorInjuries', 'TotalUninjured',
       'WeatherCondition', 'BroadPhaseOfFlight', 'ReportStatus',
       'PublicationDate'],
      dtype='object')
'''


#### Investigation Type
sns.countplot(x= xml_df["InvestigationType"])
plt.title("Accidents vs Incidents")

num_inc = len(xml_df[xml_df["InvestigationType"]=="Incident"]) #2050 Incidents
num_acc = len(xml_df[xml_df["InvestigationType"]=="Accident"]) #74207 Accidents

#Calculate percent accidents
per_acc = num_acc/num_records #96%

incidents = xml_df[xml_df["InvestigationType"]=="Incident"]
#sns.countplot(x= incidents["InjurySeverity"]) just checking if incidents have injuries

############################################################
### Identifiers
############################################################

########################## Unique Flight Idetifier: EventID 
'''
count              77257
unique             76133
top       20101022X34140
freq                   3
Name: EventId, dtype: object
'''
#################### Unique Record Idetifier: AccidentNumber 
'''
count          77257
unique         77257
top       LAX90LA318
freq               1
Name: AccidentNumber, dtype: object
'''
########### Unique Registration Idetifier: RegistrationNumber 
'''
count     77257
unique    67493
top            
freq       2756
Name: RegistrationNumber, dtype: object
'''

###########################################################
### Outcome Variables
###########################################################


##### OUTCOME VARIABLES ###################################
##### Categorical Variables () ############################

########################################### Injury Severity
'''
count         77257
unique          120
top       Non-Fatal
freq          58499
Name: InjurySeverity, dtype: object
'''

#Check out distribution of types
sns.stripplot(x= xml_df["InjurySeverity"])
plt.title("Injury Severity")

#types of severity
print(xml_df["InjurySeverity"].unique())
['' 'Non-Fatal' 'Incident' 'Fatal(1)' 'Fatal(6)' 'Fatal(2)' 'Unavailable'
 'Fatal(5)' 'Fatal(3)' 'Fatal(9)' 'Fatal(4)' 'Fatal(7)' 'Fatal(10)'
 'Fatal(43)' 'Fatal(58)' 'Fatal(295)' 'Fatal(11)' 'Fatal(8)' 'Fatal(239)'
 'Fatal(33)' 'Fatal(50)' 'Fatal(14)' 'Fatal(21)' 'Fatal(19)' 'Fatal(153)'
 'Fatal(127)' 'Fatal(28)' 'Fatal(77)' 'Fatal(12)' 'Fatal(42)' 'Fatal(157)'
 'Fatal(158)' 'Fatal(103)' 'Fatal(89)' 'Fatal(90)' 'Fatal(152)'
 'Fatal(228)' 'Fatal(17)' 'Fatal(13)' 'Fatal(24)' 'Fatal(88)' 'Fatal(65)'
 'Fatal(154)' 'Fatal(30)' 'Fatal(20)' 'Fatal(40)' 'Fatal(57)' 'Fatal(199)'
 'Fatal(114)' 'Fatal(23)' 'Fatal(102)' 'Fatal(96)' 'Fatal(49)'
 'Fatal(124)' 'Fatal(113)' 'Fatal(107)' 'Fatal(117)' 'Fatal(145)'
 'Fatal(45)' 'Fatal(160)' 'Fatal(121)' 'Fatal(16)' 'Fatal(15)'
 'Fatal(104)' 'Fatal(25)' 'Fatal(55)' 'Fatal(46)' 'Fatal(141)'
 'Fatal(115)' 'Fatal(75)' 'Fatal(71)' 'Fatal(206)' 'Fatal(138)'
 'Fatal(92)' 'Fatal(26)' 'Fatal(265)' 'Fatal(118)' 'Fatal(44)' 'Fatal(64)'
 'Fatal(18)' 'Fatal(83)' 'Fatal(143)' 'Fatal(60)' 'Fatal(131)'
 'Fatal(169)' 'Fatal(217)' 'Fatal(80)' 'Fatal(229)' 'Fatal(87)'
 'Fatal(52)' 'Fatal(97)' 'Fatal(35)' 'Fatal(29)' 'Fatal(125)' 'Fatal(349)'
 'Fatal(34)' 'Fatal(70)' 'Fatal(230)' 'Fatal(110)' 'Fatal(123)'
 'Fatal(189)' 'Fatal(72)' 'Fatal(54)' 'Fatal(68)' 'Fatal(132)' 'Fatal(37)'
 'Fatal(56)' 'Fatal(47)' 'Fatal(27)' 'Fatal(73)' 'Fatal(111)' 'Fatal(174)'
 'Fatal(144)' 'Fatal(270)' 'Fatal(156)' 'Fatal(82)' 'Fatal(256)'
 'Fatal(31)' 'Fatal(135)' 'Fatal(78)']

## divided into fatal and non fatal injuries
non_fatal = xml_df[xml_df["InjurySeverity"].str.contains("Fatal\(")==False]
fatal = xml_df[xml_df["InjurySeverity"].str.contains("Fatal\(")]

num_fatal = len(fatal)  #15409 Fatal
num_non_fatal= len(non_fatal) - num_inc #61848 - 2050 = 58798
sns.countplot(non_fatal["InjurySeverity"]) 

# calculated percentage of accidents as fatal or non fatal
# TODO: turn number of fatalities into useable format, if not otherwise stored
per_fatal = num_fatal/num_acc #21%
per_non_fatal = num_non_fatal/num_acc #79%



############################################# Aircraft Damage
'''
count           77257
unique              4
top       Substantial
freq            55420
Name: AircraftDamage, dtype: object
'''

print(xml_df["AircraftDamage"].unique())
#types of damage
#['' 'Substantial' 'Minor' 'Destroyed']
#
sns.countplot(x= xml_df["AircraftDamage"])
plt.title("Aircraft Damage")
# most have substantial damage, with about a quarter destroyed, and some minor

#made data subsets for later analysis
subs_dam = xml_df[xml_df["AircraftDamage"]=="Substantial"]
dest_dam = xml_df[xml_df["AircraftDamage"]=="Destroyed"]
minor_dam = xml_df[xml_df["AircraftDamage"]=="Minor"]

#calculated percent of accidents with damage
num_dam = len(subs_dam)+ len(dest_dam)+len(minor_dam) #74873
#per_dam = num_dam/num_acc # greater than 100%, so incidents also have damage
per_dam = num_dam/num_records #97%




##### OUTCOME VARIABLES ###################################
##### Continuous Variables (5) ############################
# Total Fatal Injuries
# Total Serious Injuries
# Total Minor Injuries
# Total Uninjured
# TODO: ---add together for total passengers?

###################################### Total Fatal Injuries 
'''
count     77257
unique      118
top           0
freq      40363
Name: TotalFatalInjuries, dtype: object
'''

#list of fatal injury types, but they are stored as strings
print(fatal["TotalFatalInjuries"].unique())
'''
[  1   6   2   5   3   9   4   7  10  43  58 295  11   8 239  33  50  14
  21  19 153 127  28  77  12  42 157 158 103  89  90 152 228  17  13  24
  88  65 154  30  20  40  57 199 114  23 102  96  49 124 113 107 117 145
  45 160 121  16  15 104  25  55  46 141 115  75  71 206 138  92  26 265
 118  44  64  18  83 143  60 131 169 217  80 229  87  52  97  35  29 125
 349  34  70 230 110 123 189  72  54  68 132  37  56  47  27  73 111 174
 144 270 156  82 256  31 135  78]
'''
## calculate most fatalities
print(max(fatal["TotalFatalInjuries"].unique())) # 349
## average number of fatalities
print(fatal["TotalFatalInjuries"].mean()) # 2.9 ~3
## most frequent number of fatalities
print(fatal["TotalFatalInjuries"].mode()) # 1
len(fatal[fatal["TotalFatalInjuries"]==1]) #7598 single fatality crashes

### distribution of fatalities
sns.stripplot(fatal["TotalFatalInjuries"])
## most accidents fewer than 30
## outliers at 349, >300
## second set between 175-300
## third tier about 30-174

#list of fatal injury types, but they are stored as strings
print(xml_df["TotalSeriousInjuries"].unique())
'''
[  0   3   1   2   5   4  15   6   7  12  50  11  66  17  27  22  18 111
  20   9  59  55  23  10  25  28  43  39  14  26  13  45   8  44  21  16
  60 106  81  47]
'''

######################################## Total Serious Injuries 
'''
count     77257
unique       41
top           0
freq      42955
Name: TotalSeriousInjuries, dtype: object
'''
## calculate most serious injuries
print(max(xml_df["TotalSeriousInjuries"].unique())) # 111
## average number of serious injuries
print(xml_df[xml_df["TotalSeriousInjuries"] >0].mean()) # 1.5 (of those with serious injuries), on these fewer than 1 fatality on avg
## most frequent number of serious injuries
print(xml_df["TotalSeriousInjuries"][xml_df["TotalSeriousInjuries"] >0].mode()) # 1
len(xml_df["TotalSeriousInjuries"][xml_df["TotalSeriousInjuries"]==1]) #7794 single serious injuries

### distribution of fatalities
sns.stripplot(xml_df["TotalSeriousInjuries"])
## most accidents fewer than 10 serious injuries
## outliers above 100 (two)
## second set between 30 and 85
## third tier about 11-29

# TODO: Come back to look at Minor and uninjured groups as necessary,
# but instead think about meaninful groupings for analysis outcome

'''
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
##### Possible geospatial/ Text Variables (2) ############
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
