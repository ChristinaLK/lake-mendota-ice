ice_cover_1855_2020.png : exports/sample.png
	cp exports/sample.png ice_cover_1855_2020.png

exports/sample.png : data/ice-dates.csv
	python3 scripts/generate-viz.py data/ice-dates.csv

data/ice-dates.csv : data/ice-raw.csv
	python3 scripts/clean-data-dates.py data/ice-raw.csv
