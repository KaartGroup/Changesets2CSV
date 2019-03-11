#!/usr/bin/env python

''' changesetApi2Csv

This tool will build out a CSV of changeset info queried based on the given parameters

Copyright (c) 2018 Kaart Group <admin@kaartgroup.com>

Released under the MIT license: http://opensource.org/licenses/mit-license.php

'''

import xml.etree.ElementTree as ET
import csv
import argparse
import urllib
import os


def changeset2Csv(file, user=None, start_time=None, end_time=None, bbox=None):
    query_params = {}
    if user:
        if user.isdigit():
            query_params['user'] = user
        else:
            query_params['display_name'] = user

    if start_time and end_time:
        query_params['time'] = ','.join([start_time, end_time])

    if bbox:
        query_params['bbox'] = ','.join(bbox)

    api_url = "https://api.openstreetmap.org/api/0.6/changesets?" + urllib.urlencode(query_params)
    changeset = urllib.urlopen(api_url).read()

    with open(file, 'w') as f:
        fieldnames = ['ID', 'Comment', 'Open', 'User', 'Created at', 'Closed at', 'Changes', 'Discussions']
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)

        root = ET.fromstring(changeset)
        csv_writer.writeheader()
        for item in root.findall('changeset'):
            changeset = {'ID': item.get('id'), 'Comment': '', 'Open': item.get('open'), 'User': item.get('user'), 'Created at': item.get('created_at'), 'Closed at': item.get('closed_at'), 'Changes': item.get('changes_count'), 'Discussions': item.get('comments_count')}

            for child in item:
                if child.get('k') == 'comment':
                    changeset['Comment'] = child.get('v').encode('utf-8')

            csv_writer.writerow(changeset)

    return True

if __name__ == "__main__":        
    
    ''' Set up arguments '''
    parser = argparse.ArgumentParser(description="Create CSV file of changeset info given query parameters.")
    parser.add_argument('output', help="Location and name of the .csv file to create ")
    parser.add_argument('-u', '--user', help="The OSM username or user id to use for the query (either username or user id, NOT both).")
    parser.add_argument('-s', '--start_time', help="The start time of the window to query (year-month-day).")
    parser.add_argument('-e', '--end_time', help="The end time of the window to query (year-month-day).")
    parser.add_argument('-b', '--bbox', nargs=4 , help="The bbox to query changesets. Values separated by spaces (min_lon min_lat max_lon max_lat).")
    args = parser.parse_args()

    if not ((args.user or args.bbox) or (args.start_time and args.end_time)):
        parser.error('No query parameters supplied: add --user, --bbox, or --start_time and --end_time.')

    if not changeset2Csv(args.output, args.user, args.start_time, args.end_time, args.bbox):
        print("There was an error creating the csv. Please contact the developer for assistance.")