# Changesets2CSV
This tool queries the Changeset API and creates a new CSV from the resulting XML.

## Requirements
This tool requires `Python 2.7.X`

## Installation
To install `changesets2CSV` on MacOS, Ubuntu, or Windows run:
```
pip install git+https://github.com/KaartGroup/Changesets2CSV
```

## Usage
```
usage: changesets2CSV.py [-h] [-u USER] [-s START_TIME] [-e END_TIME]
                        [-b BBOX BBOX BBOX BBOX]
                        output

Create CSV file of changeset info given query parameters.

positional arguments:
  output                Location and name of the .csv file to create

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  The OSM username or user id to use for the query
                        (either username or user id, NOT both).
  -s START_TIME, --start_time START_TIME
                        The start time of the window to query (YYYY-MM-DD).
  -e END_TIME, --end_time END_TIME
                        The end time of the window to query (YYYY-MM-DD).
  -b BBOX BBOX BBOX BBOX, --bbox BBOX BBOX BBOX BBOX
                        The bbox to query changesets. Values separated by
                        spaces (min_lon min_lat max_lon max_lat).
```
