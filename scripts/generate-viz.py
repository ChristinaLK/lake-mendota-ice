#!/usr/bin/env python

import math
import pandas
from datetime import datetime
import png
import sys
from pathlib import Path

# get path
#infile = '../data/ice-dates.csv'
infile = sys.argv[1]

data = pandas.read_csv(infile, usecols = ["YEAR1","CLOSEDDATE","OPENEDDATE"], 
                      parse_dates = ["CLOSEDDATE","OPENEDDATE"])

marker_month = "11"
marker_day = "20"

for state in ["CLOSED","OPENED"]:
    data[state+'OFFSET'] = data.apply(lambda x: x[state+'DATE'] - datetime.strptime(str(x['YEAR1'])+"-"+marker_month+"-"+marker_day,'%Y-%m-%d'), axis = 1)
    data[state+'NORMOFFSET'] = data.apply(lambda x: math.floor(x[state+'OFFSET'].total_seconds() / (60 * 60 * 24) / 3), axis = 1)

start_yr = int(data['YEAR1'].min())
end_yr = int(data['YEAR1'].max())
delta_min = data['CLOSEDNORMOFFSET'].min()
delta_max = data['OPENEDNORMOFFSET'].max()

height = end_yr - start_yr + 1
width = delta_max - delta_min

print(width, height)

bg_color = (0, 0, 225)
ice_color = (250, 250, 250)
lt_blue = (209, 237, 242)

color_toggle = [bg_color, ice_color]

years = list(data['YEAR1'].unique())

px = []
block_width = 3
block_height = 5
tmp_index = 5

stripe = []
for bwid in range(block_width*width):
    stripe.extend(lt_blue)

for year in years:
    change_points = []
    for i,row in data[data.YEAR1 == year].iterrows():
        for change_types in ['CLOSEDNORMOFFSET','OPENEDNORMOFFSET']:
            change_points.append(row[change_types])
    change_points.append(width+1)
    point_index = 0
    current_change_point = change_points[point_index]
    color_index = 0
    current_color = color_toggle[color_index]
    row = []
    for date in range(width):
        if date >= current_change_point:
            point_index = point_index + 1
            current_change_point = change_points[point_index]
            color_index = (color_index + 1) % 2
            current_color = color_toggle[color_index]
        for bw in range(block_width):
            row.extend(current_color)
    for bh in range(block_height):
        #print(row)
        px.append(row)
    for bh in range(block_height):
        #print(row)
        px.append(stripe)

p = Path(infile)
outfile = p.parents[1] / "exports" / "sample.png"

f = open(outfile, 'wb')
w = png.Writer(width*block_width, height*block_height*2, greyscale = False)
w.write(f, px)
f.close()

