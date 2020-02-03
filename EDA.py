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

path_to_xml_file = "./Data/AviationData.xml"
# Load xml file data

tree = et.parse(path_to_xml_file)
data = []
for el in tree.iterfind('./*'):
    for i in el.iterfind('*'):
        data.append(dict(i.items()))
df = pd.DataFrame(data)



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


Event_ID = extract_values(data, 'EventId')
narrative = extract_values(data, 'narrative')
cause = extract_values(data, 'probable_cause')


df = pd.DataFrame(list(zip(Event_ID,narrative,cause)), columns= ["Event_ID", "Narrative", "Cause"])



