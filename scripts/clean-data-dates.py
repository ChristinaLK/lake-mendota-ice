#!/usr/bin/env python3
# coding: utf-8

import pandas
from datetime import datetime
import calendar
from pathlib import Path
import sys

#datafile = "../data/ice-raw.csv"
datafile = sys.argv[1]

# read in all of the date related data
data = pandas.read_csv(datafile, na_values = '---', 
                       usecols = [0,1,2], header=0,
                       names = ["WINTER","CLOSED","OPENED"])

# remove rows that have at least one missing value
data = data[data['CLOSED'].notnull()]
data = data[data['OPENED'].notnull()]

# get the initial year into its own column
data[["YEAR1","YEAR2"]] = data['WINTER'].str.split('-', expand = True)

# generate a well-formated date for both 'CLOSED' and 'OPENED' per row
for state in ["CLOSED","OPENED"]:
    data[[state+"DAY",state+"MONSTR"]] = data[state].str.split('-', expand = True)
    def set_year(row):
        monthnum = list(calendar.month_abbr).index(row[state+'MONSTR'])
        if monthnum > 7:
            return row['YEAR1']
        else:
            return int(row['YEAR1'])+1
    data[state+'YEAR'] = data.apply(set_year,axis = 1)
    data[state+'DATE'] = data.apply(lambda x: datetime.strptime(str(x[state])+"-"+str(x[state+'YEAR']),'%d-%b-%Y'), axis = 1)
    data = data.drop([state+"DAY",state+"MONSTR",state+"YEAR"], axis = 1)

# drop extra year column
data = data.drop(['YEAR2'], axis=1)

# calculate durations
data['DURATION'] = data.apply(lambda x: x['OPENEDDATE'] - x['CLOSEDDATE'], axis =1)

# save output to data folder
p = Path(datafile)
outfile = p.parent / "ice-dates.csv"
data.to_csv(outfile, index = False)
