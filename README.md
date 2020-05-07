## Earthquakes data fetching library

In this repository you can find a tool to fetch a list of registered earthquakes from the 
[USGS](https://earthquake.usgs.gov/fdsnws/event/1/) database.

### How does it work

The program prints to the user the earthquake with highest magnitude in the past *d* days. The system tries to use 
cached data for most of its functionalities.

It also write additional information, namely a daily statistic on magnitude and a list of the highest earthquakes,
to csv files.

Using Python 3.X:
```
$ python main.py -d [days] [--no-cache] [--no-csv]
```
where:
- days: the number of days. REQUIRED
- no-cache: ignore the data cached in the database. OPTIONAL
- no-csv: do not write additional information to csv files. OPTIONAL  


#### Optional

It is possible to populate the database before running the program (avoiding most if not all the need to fetch 
information online).

Using Python 3.X:
```
$ cd scripts
$ python populate_db.py [-p | -d ]
```
where p and d are mutually exclusive and:
- p: populate the database
- d: clean the database

Note: one of the two must be provided

### Test
It is possible to test some of the implemented functionalities.

Using Python 3.X:
```
$ python -m unittest tests/test_csv.py
```
## REQUIREMENTS
Note that the project requires the ```json```, ```sqlite3``` and ```requests``` module to run. Note also that USGS limits the maximum 
number of events returned to 20000, so that it may be useless to query  for events that have an age of more than a few 
days, as only the lastest 20000 events will be returned.

