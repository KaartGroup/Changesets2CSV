#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import csv
import argparse
import requests
from cachecontrol import CacheControl
from datetime import datetime, date, timedelta
import os
import sys
import glob
import re
import time
import ssl
from xlsxwriter.workbook import Workbook
import doctest
#from tqdm import tqdm
#from defusedxml import ElementTree as ElementTree


USER_AGENT = "trackDownload/0.1 (lucas.bingham@kaartgroup.com)"
TEST_JSON_DICT = {'tags':[{'tag':'name','const':'highway'}],'users':[{'user_id':'9320902','name':'Traaker_L'}]}


def count_tag_change(changesets,tags, osm_obj_type="*",const_tag="none"):
  #Testing variables
  print_version_lists = True
  object_limit_for_query=0
  print_query = False
  dont_run_query = False
  print_query_response = False
  dont_process_query = False
  #TODO: sort data of tag changes by changeset for column data in csv
  #changesets = {<some_id>:[<objects>]}
  objects_by_changeset = {}
  #new_ver_objects = []

  #Get all objects touched in each changeset
  for changeset in changesets:
      #New changeset in list
      objects_by_changeset[changeset] = [] #?
      #Request XML for each changeset
      api_url = "https://www.openstreetmap.org/api/0.6/changeset/{changeset}/download".format(changeset=changeset)
      dev_api_url = "https://master.apis.dev.openstreetmap.org/api/0.6/changeset/{changeset}/download".format(changeset=changeset)
      api_url = api_url
      session = CacheControl(requests.session())
      result = session.get(api_url).text
      root = ET.fromstring(result)

      #If we are looking for a constant tag
      if const_tag != "none":
          #Retrieve all objects that have the tags we're looking for
          objs_modified = root.findall("./modify/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
          objs_created = root.findall("./create/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
          objs_deleted = root.findall("./delete/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))

          #Store each modified object's data in our list, new_ver_objects, as dictionaries
          for obj in objs_modified:
              this_obj = {"id":obj.attrib['id'],"version":int(obj.attrib['version'])}
              these_tags = obj.findall("tag")
              for this_tag in these_tags:
                  this_obj[this_tag.attrib['k']] = this_tag.attrib['v']

              objects_by_changeset[changeset].append(this_obj)

      #If we only care about the tag being changed
      else:
          #Retrieve all objects that have the tags we're looking for
          objs_modified = root.findall("./modify/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
          objs_created = root.findall("./create/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
          objs_deleted = root.findall("./delete/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))

          #Store each modified object's data in our list, new_ver_objects, as dictionaries
          for obj in objs_modified:
              this_obj = {"id":obj.attrib['id'],"version":int(obj.attrib['version'])}
              these_tags = obj.findall("tag")
              for this_tag in these_tags:
                  this_obj[this_tag.attrib['k']] = this_tag.attrib['v']

              objects_by_changeset[changeset].append(this_obj)


  change_count_by_changeset = {}
  #print(objects_by_changeset)

  #Count number of objects per changeset
  for this_k, this_v in objects_by_changeset.items():
      change_count_by_changeset[this_k] = len(this_v)





  #4Testing: print objects and data in new_ver_objects list
  if print_version_lists:
      print("New_Ver: ")
      for obj in objects_by_changeset: print(objects_by_changeset[obj])
      print()

  #Build query to get previous versions of all objects in new_ver_objects
  #Start of Overpass Query
  query = "[out:json][timeout:25];"
  query_count = 0
  for this_set in objects_by_changeset:
      #Build each query part for each object
      if (query_count < object_limit_for_query or object_limit_for_query == 0):
          for obj in objects_by_changeset[this_set]:

              #Can this ever happen?
              if obj["version"] > 1 and (query_count < object_limit_for_query or object_limit_for_query == 0):
                  if object_limit_for_query != 0:
                      print("Object ",query_count+1," of ",object_limit_for_query)
                  #Thank you Taylor
                  query_part = "timeline({osm_obj_type}, {osm_id}, {prev_version}); for (t['created']) {{ retro(_.val) {{ {osm_obj_type}(id:{osm_id}); out meta;}} }}"\
                  .format(osm_obj_type = osm_obj_type, osm_id = obj["id"],prev_version = int(obj["version"])-1)
                  query += query_part
                  query_count += 1

  #4Testing: print out the query and/or response
  if print_query: print(query)

  if dont_run_query == False:
      #Submit the query
      query_json = overpass_query(query)

  if print_query_response:
      if dont_run_query:
          print("Cannot print query response if it was not run")
      else:
          print(query_json)


  if dont_process_query == False and dont_run_query == False:
      #Dictionaries of id, value, version
      old_ver_objects = []
      old_objects_by_changeset = {}
      #old_objects_by_changeset{<id>:[<objects>]}
      current_set_index = 0
      objects_added = 0

      old_objects_by_changeset[changesets[current_set_index]] = []

      #Iterate through query result
      for element in query_json["elements"]:
          these_tags = element['tags']
          #print("set is ", changesets[current_set_index])
          #TODO: Grab all tags from old version objects
          this_obj = {"id":element['id'],"version":element['version']}
          for key, value in element['tags'].items():
              this_obj[key] = value

          old_objects_by_changeset[changesets[current_set_index]].append(this_obj)
          objects_added += 1

          #Ensure that we add objects to the right changeset
          if objects_added == change_count_by_changeset[changesets[current_set_index]]:
              objects_added = 0
              if current_set_index + 1 <= len(changesets) - 1:
                  current_set_index += 1
                  old_objects_by_changeset[changesets[current_set_index]] = []

      #4Testing: Print list of old-version objects
      if print_version_lists:
          print("Old_Ver: ")
          for obj in old_objects_by_changeset: print(old_objects_by_changeset[obj])
          print()

      #See what values changed
      changes_by_changeset = {}
      #Initialize change counts for all sets
      for set, changes in old_objects_by_changeset.items():
          changes_by_changeset[set] = {'added':0,'modified':0,'deleted':0}

      for set,changes in old_objects_by_changeset.items():
          this_old_set = old_objects_by_changeset[set]
          this_new_set = objects_by_changeset[set]

          for i in range(len(this_old_set)):
              for this_tag in tags:
                  #TODO: iterate through tags to check
                  if this_old_set[i].get(this_tag,False):
                      old_value = this_old_set[i][this_tag]
                  else:
                      old_value = None

                  if this_new_set[i].get(this_tag,False):
                      new_value = this_new_set[i][this_tag]
                  else:
                      new_value = None


                  #print(old_value," became ",new_value)

                  if old_value == None:
                      if new_value != None:
                          if old_value != new_value:
                              print('add')
                              changes_by_changeset[set]['added'] += 1
                          else:
                              print(old_value," didn't change")
                  else:
                      if new_value != None:
                          if old_value != new_value:
                              print('change')
                              changes_by_changeset[set]['modified'] += 1
                          else:
                              print(old_value," didn't change")
                      else:
                          if old_value != new_value:
                              print('delete')
                              changes_by_changeset[set]['deleted'] += 1
                          else:
                              print(old_value," didn't change")

      return changes_by_changeset
  else:
      return {'added':0,'modified':0,'deleted':0}


def overpass_status(api_status_url = "https://overpass-api.de/api/status"):
    """Get the overpass status -- this returns an int with the time to wait"""
    session = requests.session()
    session.headers.update({'User-Agent': USER_AGENT})
    cached_session = CacheControl(session)
    response = cached_session.get(api_status_url)
    if (response.status_code != requests.codes.ok):
        raise ValueError("Bad Request: {}".format(api_status_url))
    parsed_response = {'wait_time': []}
    for i in response.text.splitlines():
        if "Connected as" in i:
            parsed_response['connected_as'] = i.split(":")[1].strip()
        elif "Current time" in i:
            parsed_response['current_time'] = i.split(":")[1].strip()
        elif "Rate limit" in i:
            parsed_response['rate_limit'] = int(i.split(":")[1].strip())
        elif "slots available now" in i:
            parsed_response['slots_available'] = int(i.split(" ")[0].strip())
        elif "Slot available after" in i:
            parsed_response['wait_time'].append(int(i.split(" ")[5]))
    if 'slots_available' not in parsed_response:
        parsed_response['slots_available'] = 0
    wait_time = 0
    if parsed_response['rate_limit'] - parsed_response['slots_available'] >= 2 and len(parsed_response['wait_time']) > 0:
        return max(parsed_response['wait_time'])
    return wait_time

def overpass_query(query):
    """Query the overpass servers. This may block for extended periods of time, depending upon the query"""

    session = requests.session()
    session.headers.update({'User-Agent': USER_AGENT})
    cached_session = CacheControl(session)
    response = cached_session.post("http://overpass-api.de/api/interpreter", data={'data': query})
    wait_time = overpass_status()
    loop = 0
    while (wait_time > 0):
        time.sleep(wait_time)
        wait_time = overpass_status()
        loop += 1
    while (response.status_code == requests.codes.too_many_requests):
        time.sleep(10)
        response = cached_session.post("http://overpass-api.de/api/interpreter", data={'data': query})
    if (response.status_code != requests.codes.ok):
        print("Bad request")
        print(response.text)
        print(response.status_code)
        raise ValueError("Bad Request: {}".format(query))

    xml = response.text

    if (response.status_code != requests.codes.ok):
        raise ValueError("We got a bad response code of {} for {} which resulted in:\r\n{}".format(response.status_code, query, xml))
    content_type = response.headers.get('content-type')
    if content_type == 'application/osm3s+xml':
        return ET.ElementTree(ElementTree.fromstring(xml))
    elif content_type == 'application/json':
        return response.json()
    else:
        raise ValueError("Unexpected content type ({}) from the query: {}".format(content_type, query))


print(count_tag_change([72917146,72916726,72916312,72915002,72913700,72912034,72911454,72909249,72908229,72905720],["name"],"way","highway"))
