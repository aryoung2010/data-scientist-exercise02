# 1) README_Young

These files are the result of an exploratory analysis assignment undertaken
by Allison Young as part of her application for a Data Scientist postion
at the Center for Data Science at RTI International. 

The following scripts are included, as well as the final one page report.

### 2) RobinsonR44_FinalReport.pdf

This is the one-pager final report for this exercise, available as a pdf. 
The report profiles the dangers of Robinson R44 helicopters, particularly
in Brazil. (note: while I did perform external research regarding these
types of accidents- I came to this topic solely through my data analysis. 
I did not perform an internet search for this specific topic until I had
concluded my initial exploratory analysis)

### 3) DraftWebReport.html

This is a draft of how this report could become interactive in a webspace.

## 4) requirements.txt
This file includes the packages required to run these scripts in python. You
can install these automatically in cloud or other envrionments, using the code below:

#### python3 -m venv env
#### source ./env/bin/activate 
#### python -m pip install -r requirements.txt


# Included Scripts

### 5) EDA.py

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


### 6) NUSNCF_CaseStudy.py

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

### 7) BrazilHeliTextAnalysis.py

This script takes as inputs, 
1) an XML file of data downloaded
from the National Transportation Safety Board's database of 
aviation accidents.
(http://www.ntsb.gov/_layouts/ntsb.aviation/index.aspx)
2) Data in .json format from the incident narratives

Processes includes:
A) loading datasets into pandas dataframes
B) creating a case-study dataset of accidents from Brazil
C) initial steps for analyzing text logs (if there are any) from these flights

Outcomes:
This code sets up the process of analyzing text narratives from
the fatal Brazilian helicopter crashes. Ideally, I would have
liked to do a frequency analysis and some additional examination of
chunks and word grouping. However, I spent my time focusing more on 
the visualizations for this exercise report.

### 8) PrettyCharts.py

This script takes as inputs:
1) an XML file of data downloaded
from the National Transportation Safety Board's database of 
aviation accidents.
(http://www.ntsb.gov/_layouts/ntsb.aviation/index.aspx)

***** If time, text analysis output (ran out of time for this exercise)

A) loading dataset into pandas dataframes
B) creating a bar chart to illustrate interst in the Non-US, 
Non- Commercial flights, as compared to other groups
C) Map of countries with fatal helicopter crashes by fatalities
in non-us, non-commercial group

***** if time: D) Word cloud of relevant text from narrative exploration (ran out of time for this exercise)


### 9) DataDictionary.txt

This is a text version of the data dictionary from the NTSB website.
It does not take any inputs or produce any outputs

### Data Folder

This folder contains the data provided for this exercise.

### Images Folder

This folder contains the data created as a part of this analysis
