# README_Young

These files are the result of an exploratory analysis assignment undertaken
by Allison Young as part of her application for a Data Scientist postion
at the Center for Data Science at RTI International. 

The following scripts are included, as well as the final one page sreport.

# Included Scripts

### 1) EDA.py

This script takes as inputs, 
1) an XML file of data downloaded
from the National Transportation Safety Board's database of 
aviation accidents.
(http://www.ntsb.gov/_layouts/ntsb.aviation/index.aspx)
2) Data in .json format from the incident narratives

EDA Process includes:
A) loading datasets into pandas dataframes
B) exploring both outcome and predictor variables 

Outcome:
The outcome of this script was to focus on the FAR Description 
group of Non-US, Non-Commercial aircrafts, as they showed
the highest rates of fatalities for their crashes.

### 2) DataDictionary.txt

This is a text version of the data dictionary from the NTSB website.
It does not take any inputs or produce any outputs

### 3) CaseStudy.py

This script takes as inputs, 
1) an XML file of data downloaded
from the National Transportation Safety Board's database of 
aviation accidents.
(http://www.ntsb.gov/_layouts/ntsb.aviation/index.aspx)


Processes includes:
A) loading dataset into pandas dataframes
B) creating a case-study dataset of just Non-US, Non- Commercial
   flights, and comparing them to the full data set
C) examination of helicopters as a focus group, and 
    identification of variables associated with fatal accidents
    (country, make, model, weather, etc)

Outcome:
The outcome of this script was to focus on Brazilian 
helicopter accidents,particularly those that occured in 
Robinson R44 models. The final step in my analysis looks 
at text recordings from Brazilian helicopter accidents.

### 4) BrazilTextAnalysis.py

This script takes as inputs, 
1) an XML file of data downloaded
from the National Transportation Safety Board's database of 
aviation accidents.
(http://www.ntsb.gov/_layouts/ntsb.aviation/index.aspx)
2) Data in .json format from the incident narratives

Processes includes:
A) loading datasets into pandas dataframes
B) creating a case-study dataset of accidents from Brazil
C) analyzing text logs (if there are any) from these flights

### 5) PrettyCharts.py

This script takes as inputs:
1) an XML file of data downloaded
from the National Transportation Safety Board's database of 
aviation accidents.
(http://www.ntsb.gov/_layouts/ntsb.aviation/index.aspx)

***** If time, text analysis output 

A) loading dataset into pandas dataframes
B) creating a bar chart to illustrate interst in the Non-US, 
Non- Commercial flights, as compared to other groups
C) Map of countries with fatal helicopter crashes by fatalities
in non-us, non-commercial group

***** if time: D) Word cloud of relevant text from narrative exploration

Additional Visualizations created outside of python 
for summary document include:
E)Calculations of helicopter vs airplane fatalities in these groups
F) Table of high frequency makes and models for brazilian helicopter accidents, 
with helicopter graphic descriptions

## requirements.txt
This file includes the packages required to run these scripts in python. You
can install these automatically in cloud or other envrionments, using the code below:

#### python3 -m venv env
#### source ./env/bin/activate 
#### python -m pip install -r requirements.txt

