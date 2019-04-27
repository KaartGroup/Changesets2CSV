# Changesets2CSV
This tool queries the Changeset API and creates a new CSV from the resulting XML.

## Requirements
This tool requires [`Python 3.6+`](https://www.python.org/downloads/)

## Installation
To install `changesets2CSV` on MacOS, Ubuntu, or Windows run:
```
pip install git+https://github.com/KaartGroup/Changesets2CSV
```

## Usage
```
usage: changesets2CSV [-h] [-b min_lon min_lat max_lon max_lat] [-v] <command>
    

Commands for creating changeset CSV's

optional arguments:
  -h, --help            show this help message and exit
  --bbox min_lon min_lat max_lon max_lat
                        The bbox to query changesets. Values separated by
                        spaces.
  -o OUTPUT, --output OUTPUT
                        Location to create .csv files (default is current
                        location)
  -x, --excel           Create a .xlsx file.

commands:
  {specific,summary,weekly}
    specific            Specific query
    summary             Create a summary of changesets
    weekly              Create a weekly summary of changesets
```
### Example
`changesets2CSV -x weekly ../example.config`
