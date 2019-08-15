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


def count_tag_change(changesets,tag, osm_obj_type="*",const_tag="none"):
  #Testing variables
  print_version_lists = False
  print_query = False
  print_query_response = False
  object_limit_for_query=0
  dont_run_query = True
  dont_process_query = False
  #TODO: sort data of tag changes by changeset for column data in csv
  #changesets = {<some_id>:[<objects>]}
  objects_by_changeset = {}
  new_ver_objects = []

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
              tags = obj.findall("tag")
              for thisTag in tags:
                  this_obj[thisTag.attrib['k']] = thisTag.attrib['v']

              objects_by_changeset[changeset].append(this_obj)
              #new_ver_objects.append(this_obj)

          #print(changeset)
          #print(objects_by_changeset[changeset])


      #If we only care about the tag being changed
      else:
          #Retrieve all objects that have the tags we're looking for
          objs_modified = root.findall("./modify/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
          objs_created = root.findall("./create/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
          objs_deleted = root.findall("./delete/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))

          #Store each modified object's data in our list, new_ver_objects, as dictionaries
          for obj in objs_modified:
              this_obj = {"id":obj.attrib['id'],"version":int(obj.attrib['version'])}
              tags = obj.findall("tag")
              for tag in tags:
                  this_obj[tag.attrib['k']] = tag.attrib['v']

              new_ver_objects.append(this_obj)

  #print(objects_by_changeset)
  for this_k, this_v in objects_by_changeset.items():
      print(this_k,": ",this_v)


  #4Testing: print objects and data in new_ver_objects list
  if print_version_lists:
      print("New_Ver: ")
      for obj in new_ver_objects: print(obj)
      print()

  #Build query to get previous versions of all objects in new_ver_objects
  #Start of Overpass Query
  query = "[out:json][timeout:25];"
  query_count = 0
  #Build each query part for each object
  for obj in new_ver_objects:
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
          print("Cannot print query if it was not run")
      else:
          print(query_json)

  if dont_process_query == False and dont_run_query == False:
      #Dictionaries of id, value, version
      old_ver_objects = []

      #Iterate through query result
      for element in query_json["elements"]:
          these_tags = element['tags']
          #If tag is present in this version
          if these_tags.get(tag,None) != None:
              old_ver_objects.append({"id":element['id'],'value':element['tags'][tag],"version":element['version']})
          #If tag is not present in this version
          else:
              old_ver_objects.append({"id":element['id'],'value':None,"version":element['version']})
      #4Testing: Print list of old-version objects
      if print_version_lists:
          print("Old_Ver: ")
          for obj in old_ver_objects: print(obj)
          print()

      #See what values changed
      changes = {'added':0,'modified':0,'deleted':0}
      for i in range(len(old_ver_objects)):
          old_value = old_ver_objects[i]["value"]
          if new_ver_objects[i].get(tag,False):
              new_value = new_ver_objects[i][tag]
          else:
              new_value = None

          if old_value == None:
              if new_value != None:
                  print('add')
                  changes['added'] += 1
          else:
              if new_value != None:
                  print('change')
                  changes['modified'] += 1
              else:
                  print('delete')
                  changes['deleted'] += 1

          if old_value != new_value:
              print(old_value," became ",new_value)
          else:
              print(old_value, "didn't change")

      #TODO: have this return a dictionary that lists add/mod/del tag for each changeset
      #changeset_tag_changes = {12345:{'tag_added':0,'tag_modified':0,'tag_deleted':0}}
      return changes
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

print(count_tag_change([72917146,72916726,72916312,72915002,72913700,72912034,72911454,72909249,72908229,72905720],"name","way","highway"))