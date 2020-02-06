#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 21:53:17 2020

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
#  B) creating a case-study dataset of accidents from Brazil
#  C) analyzing text logs (if there are any) from these flights
# 
#
# 
############################################################
#### SUMMARY FINDINGS 
############################################################
#
#
#
#
#
#


##########################################################
#### CODE ################################################
##########################################################
## Import Files
import json
import pandas as pd
import xml.etree.ElementTree as et
from nltk import word_tokenize
from nltk.corpus import stopwords
#nltk.download()
import matplotlib
matplotlib.use('agg')


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

brazil = nuncf[nuncf["Country"]=="Brazil"] #110 Accidents

brazil_fatal = brazil[brazil["TotalFatalInjuries"]> 0] #101 

## 92% of Brazilian Accidents are Fatal

#json_df.head(1) ## Event_Id is in both

brazil_fatal.head(1) ##Event_Id is the same

brazil_fatal_list = list(brazil_fatal["EventId"].unique())

## 100 Ids to merge with Ids in the text


###########################################################
### Convert JSON data from single file to pandas DataFrame
###########################################################

#load json file to object

### 145 json files, start at 499, add 500 each time

#create a master dataframe to hold all the .json data from the files in the
# data folder
master_json = pd.DataFrame(columns= ["Event_ID", "Narrative", "Cause"])


  
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

## iterate through each file, extract the data, and append to master file
for i in range (1,143):
    fnum = (i*500)-1
    with open('./data/NarrativeData_{}.json'.format(fnum)) as f:
        data = json.load(f)
  
    #field lists for each set of json values
    Event_ID = extract_values(data, 'EventId')
    narrative = extract_values(data, 'narrative')
    cause = extract_values(data, 'probable_cause')

    #combine lists into a pandas dataframe
    json_df = pd.DataFrame(list(zip(Event_ID,narrative,cause)), columns= ["Event_ID", "Narrative", "Cause"])
    master_json= master_json.append(json_df)
    print("File {} added".format(fnum))

##add the last file, which doesn't follow the naming convention of others
with open('./data/NarrativeData_999999.json') as f:
        data = json.load(f)
  
#field lists for each set of json values
Event_ID = extract_values(data, 'EventId')
narrative = extract_values(data, 'narrative')
cause = extract_values(data, 'probable_cause')

#combine lists into a pandas dataframe
json_df = pd.DataFrame(list(zip(Event_ID,narrative,cause)), columns= ["Event_ID", "Narrative", "Cause"])
master_json= master_json.append(json_df)
print("File 999999 added".format(fnum))
    

#check the length of the master file
print(len(master_json))

##71,133 files

############ Combine text and xml file data to create corpus

corpus = brazil_fatal.merge(master_json, left_on='EventId', right_on='Event_ID', how='inner')
##93 of 100 matched- not bad!

#preview a corpus record, and test text methods on first narrative

corpus.head(1)
# No cause records, it appears all narratives from Brazil have a similar text 
# format, as illustrated by the first one below.
#text = corpus['Narrative'][0]
#print(text)
'''
The foreign authority was the source of this information.
On July 19, 2015, at 2115 local time, a Cessna 210D, Brazilian registration 
PR-ITO, was destroyed when it impacted terrain during a go-around at 
General Leite De Castro Airport (SWLC), Goiás, Brazil. The Mexican pilot 
incurred minor injuries, while the Colombian passenger was fatally injured. 
The flight, which originated at Jundiaí Airport, Jundiaí, São Paulo, Brazil, 
was being conducted under Brazilian flight regulations.
'''

#set stopwords to English languate
#a= set(stopwords.words('english'))

# Convert text to lowercase
#text1= word_tokenize(text.lower())
#print(text1)

## stopwords may be handy for looking at any perhaps cities or other key words
# relavent to circumstances in weather or accident causes
#stopwords = [x for x in text1 if x not in a]
#print (stopwords)

['foreign', 'authority', 'source', 'information.on', 'july', '19', ',',
 '2015', ',', '2115', 'local', 'time', ',', 'cessna', '210d', ',', 'brazilian',
 'registration', 'pr-ito', ',', 'destroyed', 'impacted', 'terrain', 
 'go-around', 'general', 'leite', 'de', 'castro', 'airport', '(', 'swlc', ')',
 ',', 'goiás', ',', 'brazil', '.', 'mexican', 'pilot', 'incurred', 'minor', 
 'injuries', ',', 'colombian', 'passenger', 'fatally', 'injured', '.', 
 'flight', ',', 'originated', 'jundiaí', 'airport', ',', 'jundiaí', ',', 
 'são', 'paulo', ',', 'brazil', ',', 'conducted', 'brazilian', 'flight', 
 'regulations', '.']

all_words = list()

a= set(stopwords.words('english'))

for i in range(len(corpus)):   
    text = corpus['Narrative'][i]
    #print(text)
    text1 = word_tokenize(text.lower())
    #print(text1)
    stopwords_c = [x for x in text1 if x not in a]
   # print(stopwords)
    all_words= all_words.append(stopwords_c)
    print("Narrative {} added to list".format(i))
    
