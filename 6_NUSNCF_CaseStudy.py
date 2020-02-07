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
# 
#
# Processes includes:
#  A) loading dataset into pandas dataframes
#  B) creating a case-study dataset of just Non-US, Non- Commercial
#   flights, and comparing them to the full data set
#  C) examination of helicopters as a focus group, and 
#   identification of variables associated with fatal accidents
#   (country, make, model, weather, etc)
# 
# Outcome:
#  The outcome of this script was to focus on Brazilian 
#  helicopter accidents,particularly those that occured in 
#  Robinson R44 models. The final step in my analysis looks 
#  at text recordings from Brazilian helicopter accidents.
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
# Subject Experts
# In a real-life project, this would be the point in the project when I would
# want to speak with a subject matter expert to gain insight into what kind of
# flights this designation describes.

# Case Study Findings
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

# create list of columns
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

#create a dataset of all accidents, and a group for just non us non 
# commercial flight aand incident ccident reoprts
accidents = xml_df[xml_df["InvestigationType"]=="Accident"] #7420 Accidents
nuncf = xml_df[xml_df["FARDescription"]=="Non-U.S., Non-Commercial"] #667
## 9% of Accidents are from this group

print(accidents["TotalFatalInjuries"].sum()) #43995
print(nuncf["TotalFatalInjuries"].sum()) #1284
## 3% of all fatalities

print(len(accidents[accidents["TotalFatalInjuries"]>0])) #15409
print(len(nuncf[nuncf["TotalFatalInjuries"]>0])) #512
## 3% of all crashes

## But 77% of crashes are fatal! 
## So that is why we are looking at these groups...

## lets look at this group a little more

#explore stats for just this group
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


## Look at how many aircraft categories there are for this
## group as compared to all reports
print(xml_df["AircraftCategory"].describe())
print(nuncf["AircraftCategory"].describe())

'''
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
'''

## fewer groups, so can probably look into them directly
print(nuncf["AircraftCategory"].unique())
#['Helicopter' 'Airplane' '' 'Balloon']

## here we see the deadly impact of helicoptor flights in NUNCF
print(nuncf[nuncf["AircraftCategory"]=="Helicopter"].sum())
print(len(nuncf[nuncf["AircraftCategory"]=="Helicopter"])) #153

#TotalFatalInjuries                                271
#TotalSeriousInjuries                               44
#TotalMinorInjuries                                 47
#TotalUninjured                                     81

#61% of passengers in accidents died 271/443 passengers

## Compare to Airplanes
print(nuncf[nuncf["AircraftCategory"]=="Airplane"].sum())
print(len(nuncf[nuncf["AircraftCategory"]=="Airplane"])) #434

#TotalFatalInjuries                               842
#TotalSeriousInjuries                             120
#TotalMinorInjuries                                66
#TotalUninjured                                   393                                                47

# 59% of airline accicents were fatal       842/1421 passengers


# Okay, so let's look at Non-US, Non-Commercial Helicopter Accidents

# create a helicopter only dataset
nuncf_heli = nuncf[nuncf["AircraftCategory"]=="Helicopter"]

nuncf_heli = nuncf_heli[nuncf_heli["InvestigationType"]=="Accident"]
#Now we are looking at 150 records for this population


# again review stats
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
## see list of countries in this group
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
### look at fataal accidents, total fatalities, and calculate % accidents that 
## are fatal
print(nuncf_heli[nuncf_heli["TotalFatalInjuries"]>0].groupby('Country')["TotalFatalInjuries"].count().sort_values(ascending=False))
print(nuncf_heli.groupby('Country')["TotalFatalInjuries"].sum().sort_values(ascending=False))
print(nuncf_heli.groupby('Country')["EventId"].count().sort_values(ascending=False))

'''
Country   Fatal_Accidents   Fatalities    Accidents    % Fatal
Brazil                19    43             20              95%
Australia             10    16             12              83%
Russia                 9    25             12              75%
Germany                6    12             7               86%
Colombia               6    17             7               86%
United Kingdom         5    17             7               71%
Venezuela              4    13             6               67%
Spain                  4    6              4              100%
France                 4    9              4              100%
Malaysia               3    5              3              100%
Mexico                 3    6              8               38%
Chile                  3    18             5               60%
Italy                  3    8              3              100%
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
# I wonder if they have something regularly going on with helicopters


## trim data more to just Brazil
brazil_heli= nuncf_heli[nuncf_heli["Country"]=="Brazil"]

print(brazil_heli["Make"].unique())

['BELL' 'ROBINSON' 'AGUSTA' 'EMBRAER']
## only 4 types of helicopters used

## look at fatal accidents by make and model

print(brazil_heli.groupby('Make')["TotalFatalInjuries"].count().sort_values(ascending=False))
print(brazil_heli.groupby('Make')["EventId"].count().sort_values(ascending=False))

'''
Fatal Accidents by Make
ROBINSON    13
BELL         5
EMBRAER      1
AGUSTA       1
Name: TotalFatalInjuries, dtype: int64
'''

print(brazil_heli["Model"].unique())
'''
['206B' 'R44 - II' 'R22 - BETA' 'R44' 'R66' '212' 'R22' 'AW119MKII' '206'
 'EMB-720']
'''

print(brazil_heli.groupby(['Make','Model'])["TotalFatalInjuries"].count().sort_values(ascending=False))

### Robinson R44 comes up strong in the data- more than half of the 
### fatal accidents

'''
FatalAccidents by Make and Model
Make      Model     
ROBINSON  R44           7
BELL      206B          3
ROBINSON  R66           2
          R22 - BETA    2
          R44 - II      1
          R22           1
EMBRAER   EMB-720       1
BELL      212           1
          206           1
AGUSTA    AW119MKII     1
Name: TotalFatalInjuries, dtype: int64
'''

# look at purpose, maybe these models are specific for a use
print(brazil_heli["PurposeOfFlight"].unique())
'''
['Personal' 'Instructional' 'Unknown' 'Business' 'Aerial Observation'
 'Other Work Use']
'''

print(brazil_heli.groupby(['PurposeOfFlight','Make'])["TotalFatalInjuries"].count().sort_values(ascending=False))
'''
Top # Fatal Accidents by Purpose and Make
Unknown             ROBINSON    5
Personal            ROBINSON    4
Unknown             BELL        2
Instructional       ROBINSON    2
'''
## nothing really meaningful here
## Well Unknown could be rescues or something? But seems like
# that theory may be shakey.

print(brazil_heli.groupby(['BroadPhaseOfFlight'])["TotalFatalInjuries"].count().sort_values(ascending=False))
# Weather, Schedule, Phase of flight mostly unknown


#############
############# Story Check
############# Are Airplanes Similar to Helicopters?
#############

brazil = nuncf[nuncf["Country"]== 'Brazil']
#110


## compare number of brazilian airplans to helicopters
print(brazil.groupby(['AircraftCategory'])["EventId"].count().sort_values(ascending=False))

#Accidents by type
#AircraftCategory
#Airplane      77
#Helicopter    20

## cessnas also appear frequently- but they are one of the most popular
## personal aircraft models out there.
brazil_air = nuncf[nuncf["AircraftCategory"]=="Airplane"]
print(brazil_air.groupby(['PurposeOfFlight','Make'])["TotalFatalInjuries"].count().sort_values(ascending=False))
'''
Fatal Accidents by Purpose and Make
PurposeOfFlight          Make                          
Unknown                  CESSNA                            51
Personal                 CESSNA                            32
                         PIPER                             25
Unknown                  PIPER                             24
Personal                 BEECH                             14
                         Cessna                            14
Instructional            CESSNA                            13
Personal                 Piper                             10
Unknown                  BEECH                             10
Aerial Application       CESSNA                             9
Instructional            PIPER                              9
Business                 CESSNA                             8
'''
  
## Cessna 172 may be an additional route to look into               
print(brazil_air.groupby(['Make','Model'])["TotalFatalInjuries"].count().sort_values(ascending=False))

'''
Make                            Model            
CESSNA                          172                  14
                                182                   9
                                210                   8
CIRRUS                          SR22                  7
CESSNA                          150                   6
BEECH                           A36                   6
CESSNA                          172N                  5
PIPER                           PA34                  5
BEECH                           58                    5
AIR TRACTOR                     AT802                 4
CESSNA                          A188B                 4
Cessna                          182                   3
CESSNA                          152                   3
CIRRUS                          SR20                  3
PIPER                           PA-30                 3
                                PA-34                 3
EMBRAER                         EMB711                3
CESSNA                          T206H                 3
                                210N                  3
                                172R                  3
PIPER                           PA28R                 3
Cessna                          152                   3
'''
