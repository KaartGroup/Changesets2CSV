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

print_version_lists = False
print_query = False
print_query_response = False
object_limit_for_query=0
dont_run_query = False
dont_process_query = False

def count_tag_change(changeset,tag, osm_obj_type="*",const_tag="none"):
  api_url = "https://www.openstreetmap.org/api/0.6/changeset/{changeset}/download".format(changeset=changeset)
  dev_api_url = "https://master.apis.dev.openstreetmap.org/api/0.6/changeset/{changeset}/download".format(changeset=changeset)
  api_way_url = "https://www.openstreetmap.org/api/0.6/way/"
  api_url = api_url
  session = CacheControl(requests.session())
  result = session.get(api_url).text
  root = ET.fromstring(result)

  #Dictionaries of id, value, version
  new_ver_objects = []
  if const_tag != "none":
      objs_modified = root.findall("./modify/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
      objs_created = root.findall("./create/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
      objs_deleted = root.findall("./delete/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))

      print(len(objs_created)," created. ",len(objs_deleted)," deleted.",len(objs_modified)," modified.")

      for obj in objs_modified:
          #print("way ",obj.attrib["id"])
          this_obj = {"id":obj.attrib['id'],"version":int(obj.attrib['version'])}
          tags = obj.findall("tag")
          for thisTag in tags:
              this_obj[thisTag.attrib['k']] = thisTag.attrib['v']
              #print(tag.attrib["k"],": ",tag.attrib["v"])

          new_ver_objects.append(this_obj)

  else:
      objs_modified = root.findall("./modify/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
      objs_created = root.findall("./create/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
      objs_deleted = root.findall("./delete/{osm_obj_type}".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
      for obj in objs_modified:
          #print("way ",obj.attrib["id"])
          this_obj = {"id":obj.attrib['id'],"version":int(obj.attrib['version'])}
          tags = obj.findall("tag")
          for tag in tags:
              this_obj[tag.attrib['k']] = tag.attrib['v']
              #print(tag.attrib["k"],": ",tag.attrib["v"])

          new_ver_objects.append(this_obj)

      for obj in new_ver_objects:
          print(obj)


  if print_version_lists:
      print("New_Ver: ")
      for obj in new_ver_objects: print(obj)
      print()

  query = "[out:json][timeout:25];"
  query_count = 0
  for obj in new_ver_objects:
      #Can this ever happen?
      if obj["version"] > 1 and (query_count < object_limit_for_query or object_limit_for_query == 0):
          if object_limit_for_query != 0:
              print("Object ",query_count+1," of ",object_limit_for_query)
          query_part = "timeline({osm_obj_type}, {osm_id}, {prev_version}); for (t['created']) {{ retro(_.val) {{ {osm_obj_type}(id:{osm_id}); out meta;}} }}"\
          .format(osm_obj_type = osm_obj_type, osm_id = obj["id"],prev_version = int(obj["version"])-1)
          query += query_part
          query_count += 1
  if print_query: print(query)

  if dont_run_query == False:
      query_json = overpass_query(query)

  if print_query_response:
      if dont_run_query:
          print("Cannot print query if it was not run")
      else:
          print(query_json)

  if dont_process_query == False and dont_run_query == False:
      #Dictionaries of id, value, version
      old_ver_objects = []
      for element in query_json["elements"]:
          these_tags = element['tags']
          if these_tags.get(tag,None) != None:
              old_ver_objects.append({"id":element['id'],'value':element['tags'][tag],"version":element['version']})
          else:
              old_ver_objects.append({"id":element['id'],'value':None,"version":element['version']})
      if print_version_lists:
          print("Old_Ver: ")
          for obj in old_ver_objects: print(obj)
          print()

      #See what values changed
      changed_values = 0
      for i in range(len(old_ver_objects)):
          old_value = old_ver_objects[i]["value"]
          if new_ver_objects[i].get(tag,False):
              new_value = new_ver_objects[i][tag]
          else:
              new_value = None

          '''
          new_value = new_ver_objects[i][tag]
          '''
          if old_value != new_value:
              print(old_value," became ",new_value)
              changed_values += 1
          else:
              print(old_value, "didn't change")

      return changed_values
  else:
      return 0



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

name_changes = count_tag_change(73198966,"name","way","highway")
print(name_changes," names were changed in this changeset")
