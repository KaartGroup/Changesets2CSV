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
TEST_JSON_DICT = {'tags':[{'tag':'name','const':'highway'},{'tag':'surface','const':'highway'}],'users':[{'user_id':'9320902','name':'Traaker_L'}]}
#,{'tag':'surface','const':'highway'}
HARDCODED_QUERY_RESULT = {
  "version": 0.6,
  "generator": "Overpass API 0.7.55.7 8b86ff77",
  "osm3s": {
    "timestamp_osm_base": "2019-08-16T21:49:02Z",
    "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL."
  },
  "elements": [

{
  "type": "way",
  "id": 596686748,
  "timestamp": "2018-06-12T01:15:25Z",
  "version": 1,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683563959,
    5683563958,
    5683563960,
    445225564
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596686748,
  "timestamp": "2018-06-12T01:15:25Z",
  "version": 1,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683563959,
    5683563958,
    5683563960,
    445225564
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596686747,
  "timestamp": "2018-06-12T01:34:24Z",
  "version": 2,
  "changeset": 59757887,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    4538571793,
    5683563957,
    5683580081,
    5683563956
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 616496954,
  "timestamp": "2019-08-01T21:57:41Z",
  "version": 2,
  "changeset": 72916312,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5828596776,
    1720269664
  ],
  "tags": {
    "lanes": "2",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 709758406,
  "timestamp": "2019-08-01T21:57:41Z",
  "version": 3,
  "changeset": 72916312,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    445223481,
    5683563839,
    6672720435,
    5683563843,
    4538571793,
    282894616
  ],
  "tags": {
    "highway": "tertiary",
    "lanes": "2",
    "motor_vehicle:forward": "no",
    "name": "Phố Sa Đôi",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596686747,
  "timestamp": "2018-06-12T01:34:24Z",
  "version": 2,
  "changeset": 59757887,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    4538571793,
    5683563957,
    5683580081,
    5683563956
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 616496954,
  "timestamp": "2019-08-01T21:57:41Z",
  "version": 2,
  "changeset": 72916312,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5828596776,
    1720269664
  ],
  "tags": {
    "lanes": "2",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 709758406,
  "timestamp": "2019-08-01T21:57:41Z",
  "version": 3,
  "changeset": 72916312,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    445223481,
    5683563839,
    6672720435,
    5683563843,
    4538571793,
    282894616
  ],
  "tags": {
    "highway": "tertiary",
    "lanes": "2",
    "motor_vehicle:forward": "no",
    "name": "Phố Sa Đôi",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596686745,
  "timestamp": "2018-06-12T01:15:25Z",
  "version": 1,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683563954,
    5683563953,
    5683563952
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 616496954,
  "timestamp": "2018-08-13T05:57:30Z",
  "version": 1,
  "changeset": 61613114,
  "user": "marupally",
  "uid": 7795534,
  "nodes": [
    5828596776,
    1720269664
  ],
  "tags": {
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 616496955,
  "timestamp": "2018-08-13T05:57:30Z",
  "version": 1,
  "changeset": 61613114,
  "user": "marupally",
  "uid": 7795534,
  "nodes": [
    282894616,
    5828596776
  ],
  "tags": {
    "layer": "1",
    "highway": "tertiary",
    "bridge": "yes"
  }
},
{
  "type": "way",
  "id": 709758406,
  "timestamp": "2019-08-01T21:00:32Z",
  "version": 2,
  "changeset": 72915002,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    445223481,
    5683563839,
    5683563843,
    4538571793,
    282894616
  ],
  "tags": {
    "highway": "tertiary",
    "lanes": "2",
    "motor_vehicle:forward": "no",
    "name": "Phố Sa Đôi",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 457742003,
  "timestamp": "2019-04-19T07:05:58Z",
  "version": 3,
  "changeset": 69367112,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    1720269664,
    4538405071,
    1720269694
  ],
  "tags": {
    "name": "Ngõ 252",
    "service": "alley",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 37926679,
  "timestamp": "2019-04-19T06:40:54Z",
  "version": 8,
  "changeset": 69366651,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    445225637,
    4539925542,
    445225564,
    5683563954,
    1720269664
  ],
  "tags": {
    "name": "Phố Sa Đôi",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 596686745,
  "timestamp": "2018-06-12T01:15:25Z",
  "version": 1,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683563954,
    5683563953,
    5683563952
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 616496954,
  "timestamp": "2018-08-13T05:57:30Z",
  "version": 1,
  "changeset": 61613114,
  "user": "marupally",
  "uid": 7795534,
  "nodes": [
    5828596776,
    1720269664
  ],
  "tags": {
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 616496955,
  "timestamp": "2018-08-13T05:57:30Z",
  "version": 1,
  "changeset": 61613114,
  "user": "marupally",
  "uid": 7795534,
  "nodes": [
    282894616,
    5828596776
  ],
  "tags": {
    "layer": "1",
    "highway": "tertiary",
    "bridge": "yes"
  }
},
{
  "type": "way",
  "id": 709758406,
  "timestamp": "2019-08-01T21:00:32Z",
  "version": 2,
  "changeset": 72915002,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    445223481,
    5683563839,
    5683563843,
    4538571793,
    282894616
  ],
  "tags": {
    "highway": "tertiary",
    "lanes": "2",
    "motor_vehicle:forward": "no",
    "name": "Phố Sa Đôi",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 457742003,
  "timestamp": "2019-04-19T07:05:58Z",
  "version": 3,
  "changeset": 69367112,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    1720269664,
    4538405071,
    1720269694
  ],
  "tags": {
    "name": "Ngõ 252",
    "service": "alley",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 37926679,
  "timestamp": "2019-04-19T06:40:54Z",
  "version": 8,
  "changeset": 69366651,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    445225637,
    4539925542,
    445225564,
    5683563954,
    1720269664
  ],
  "tags": {
    "name": "Phố Sa Đôi",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 356005211,
  "timestamp": "2015-06-24T11:39:09Z",
  "version": 1,
  "changeset": 32181317,
  "user": "Hieu Van",
  "uid": 2678766,
  "nodes": [
    1720261420,
    1720261377,
    1720261369,
    1720261410,
    1720261315,
    1720261416,
    1720261338
  ],
  "tags": {
    "highway": "path"
  }
},
{
  "type": "way",
  "id": 596297056,
  "timestamp": "2018-06-11T05:54:53Z",
  "version": 1,
  "changeset": 59728326,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5681023548,
    5681023547,
    5681023546,
    5681023545
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684700540,
  "timestamp": "2019-04-19T04:43:23Z",
  "version": 1,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    6415482256,
    6415482246
  ],
  "tags": {
    "name": "Ngõ 59",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes"
  }
},
{
  "type": "way",
  "id": 709758406,
  "timestamp": "2019-08-01T18:50:06Z",
  "version": 1,
  "changeset": 72911454,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    445223481,
    5683563839,
    5683563843,
    4538571793,
    282894616
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Sa Đôi"
  }
},
{
  "type": "way",
  "id": 596297054,
  "timestamp": "2018-06-12T01:15:27Z",
  "version": 2,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5681023544,
    5681023542,
    5683563838,
    5681023543
  ],
  "tags": {
    "highway": "service"
  }
},
{
  "type": "way",
  "id": 684700534,
  "timestamp": "2019-08-01T20:10:12Z",
  "version": 2,
  "changeset": 72913700,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    6415482253,
    6415482243
  ],
  "tags": {
    "name": "Ngõ 56 Đại Linh",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes"
  }
},
{
  "type": "way",
  "id": 355926531,
  "timestamp": "2019-08-01T18:50:06Z",
  "version": 3,
  "changeset": 72911454,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    3614458992,
    5681023581,
    5681023532,
    3614460893,
    3614460894
  ],
  "tags": {
    "highway": "residential",
    "service": "driveway",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 596689227,
  "timestamp": "2019-08-01T20:10:12Z",
  "version": 3,
  "changeset": 72913700,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580043,
    5683580042,
    5683580041,
    5683580040,
    5683580039,
    5683580044,
    5683580038,
    4538570234
  ],
  "tags": {
    "name": "Ngõ 44 Đại Linh",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes"
  }
},
{
  "type": "way",
  "id": 596689241,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 3,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580081,
    5683580080,
    5683580079,
    5683580078,
    5683580077,
    5683580072,
    5683580076,
    5683580075,
    5683580074,
    5683580073
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 310168314,
  "timestamp": "2019-08-01T20:10:12Z",
  "version": 13,
  "changeset": 72913700,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    3155466740,
    5721894149,
    5721894147,
    5681231708,
    106068260,
    1720261338,
    282894611,
    3614460894,
    5681023545,
    5681023543,
    5683563830,
    5683563827,
    445223481
  ],
  "tags": {
    "hgv:conditional": "no @ (06:30-09:30,16:00-19:00)",
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Sa Đôi",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 356005211,
  "timestamp": "2015-06-24T11:39:09Z",
  "version": 1,
  "changeset": 32181317,
  "user": "Hieu Van",
  "uid": 2678766,
  "nodes": [
    1720261420,
    1720261377,
    1720261369,
    1720261410,
    1720261315,
    1720261416,
    1720261338
  ],
  "tags": {
    "highway": "path"
  }
},
{
  "type": "way",
  "id": 596297056,
  "timestamp": "2018-06-11T05:54:53Z",
  "version": 1,
  "changeset": 59728326,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5681023548,
    5681023547,
    5681023546,
    5681023545
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684700540,
  "timestamp": "2019-04-19T04:43:23Z",
  "version": 1,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    6415482256,
    6415482246
  ],
  "tags": {
    "name": "Ngõ 59",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes"
  }
},
{
  "type": "way",
  "id": 709758406,
  "timestamp": "2019-08-01T18:50:06Z",
  "version": 1,
  "changeset": 72911454,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    445223481,
    5683563839,
    5683563843,
    4538571793,
    282894616
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Sa Đôi"
  }
},
{
  "type": "way",
  "id": 596297054,
  "timestamp": "2018-06-12T01:15:27Z",
  "version": 2,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5681023544,
    5681023542,
    5683563838,
    5681023543
  ],
  "tags": {
    "highway": "service"
  }
},
{
  "type": "way",
  "id": 684700534,
  "timestamp": "2019-08-01T20:10:12Z",
  "version": 2,
  "changeset": 72913700,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    6415482253,
    6415482243
  ],
  "tags": {
    "name": "Ngõ 56 Đại Linh",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes"
  }
},
{
  "type": "way",
  "id": 355926531,
  "timestamp": "2019-08-01T18:50:06Z",
  "version": 3,
  "changeset": 72911454,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    3614458992,
    5681023581,
    5681023532,
    3614460893,
    3614460894
  ],
  "tags": {
    "highway": "residential",
    "service": "driveway",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 596689227,
  "timestamp": "2019-08-01T20:10:12Z",
  "version": 3,
  "changeset": 72913700,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580043,
    5683580042,
    5683580041,
    5683580040,
    5683580039,
    5683580044,
    5683580038,
    4538570234
  ],
  "tags": {
    "name": "Ngõ 44 Đại Linh",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes"
  }
},
{
  "type": "way",
  "id": 596689241,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 3,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580081,
    5683580080,
    5683580079,
    5683580078,
    5683580077,
    5683580072,
    5683580076,
    5683580075,
    5683580074,
    5683580073
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 310168314,
  "timestamp": "2019-08-01T20:10:12Z",
  "version": 13,
  "changeset": 72913700,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    3155466740,
    5721894149,
    5721894147,
    5681231708,
    106068260,
    1720261338,
    282894611,
    3614460894,
    5681023545,
    5681023543,
    5683563830,
    5683563827,
    445223481
  ],
  "tags": {
    "hgv:conditional": "no @ (06:30-09:30,16:00-19:00)",
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Sa Đôi",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596686700,
  "timestamp": "2018-06-12T01:15:23Z",
  "version": 1,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683563827,
    5683563826,
    5683563825
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596689235,
  "timestamp": "2018-06-12T01:34:23Z",
  "version": 1,
  "changeset": 59757887,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683580058,
    5683580057
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684700534,
  "timestamp": "2019-04-19T04:43:22Z",
  "version": 1,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    6415482253,
    6415482243
  ],
  "tags": {
    "name": "Ngõ 56",
    "motorcycle": "yes",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 709758407,
  "timestamp": "2019-08-01T18:50:06Z",
  "version": 1,
  "changeset": 72911454,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    445223320,
    5683580045,
    6671462008,
    5683580049
  ],
  "tags": {
    "name": "Ngõ 28",
    "hgv": "no",
    "highway": "residential",
    "maxweight": "1",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689227,
  "timestamp": "2019-04-19T04:43:23Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580043,
    5683580042,
    5683580041,
    5683580040,
    5683580039,
    5683580044,
    5683580038,
    4538570234
  ],
  "tags": {
    "name": "Ngõ 44",
    "motorcycle": "yes",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 596689233,
  "timestamp": "2019-04-19T04:43:24Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580054,
    5683580053,
    5683580052
  ],
  "tags": {
    "highway": "service"
  }
},
{
  "type": "way",
  "id": 616496953,
  "timestamp": "2019-04-19T04:43:24Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    4538570236,
    5828596775,
    5828596774
  ],
  "tags": {
    "name": "Ngõ 93",
    "motorcycle": "yes",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 675323607,
  "timestamp": "2019-04-19T04:43:23Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    445223320,
    6415482257,
    6415482256,
    4538570234,
    6415482254,
    4538570235
  ],
  "tags": {
    "name": "Phố Đại Linh",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 684700530,
  "timestamp": "2019-08-01T17:41:10Z",
  "version": 2,
  "changeset": 72909249,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    6415482254,
    6415482250,
    6415482252,
    6415482248,
    6415482244,
    6415482255,
    6415482237,
    6415482245
  ],
  "tags": {
    "name": "Ngõ 69",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 684702462,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 2,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580071,
    4538570239
  ],
  "tags": {
    "name": "Ngõ 127",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 684702463,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 2,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580070,
    5683580069
  ],
  "tags": {
    "name": "Ngõ 125",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 684702464,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 2,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    6415499210,
    6415499209
  ],
  "tags": {
    "name": "Ngõ 66",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689232,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 3,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580051,
    445223188
  ],
  "tags": {
    "name": "Ngõ 54",
    "highway": "residential",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689238,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 3,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580068,
    5683580062,
    5683580067
  ],
  "tags": {
    "name": "Ngõ 119",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 596689237,
  "timestamp": "2019-08-01T19:07:32Z",
  "version": 4,
  "changeset": 72912034,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580066,
    5683580065,
    5683580064,
    5683580059,
    6672087146,
    5683580063
  ],
  "tags": {
    "name": "Ngõ 97",
    "highway": "residential",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 596689239,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 4,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580071,
    6670677780,
    5683580070
  ],
  "tags": {
    "name": "Ngõ 127",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 402425921,
  "timestamp": "2019-07-31T16:06:34Z",
  "version": 10,
  "changeset": 72863792,
  "user": "ReedtheRiver",
  "uid": 9965337,
  "nodes": [
    445223386,
    6665925702,
    6415482251,
    5722094034,
    6415482249,
    445223320
  ],
  "tags": {
    "name": "Đại Linh",
    "highway": "tertiary",
    "lanes": "2",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 310168314,
  "timestamp": "2019-08-01T18:50:06Z",
  "version": 12,
  "changeset": 72911454,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    3155466740,
    5721894149,
    5721894147,
    5681231708,
    106068260,
    1720261338,
    282894611,
    3614460894,
    5681023545,
    5681023543,
    5683563830,
    5683563827,
    445223481
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Sa Đôi"
  }
},
{
  "type": "way",
  "id": 596686700,
  "timestamp": "2018-06-12T01:15:23Z",
  "version": 1,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683563827,
    5683563826,
    5683563825
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596689235,
  "timestamp": "2018-06-12T01:34:23Z",
  "version": 1,
  "changeset": 59757887,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683580058,
    5683580057
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684700534,
  "timestamp": "2019-04-19T04:43:22Z",
  "version": 1,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    6415482253,
    6415482243
  ],
  "tags": {
    "name": "Ngõ 56",
    "motorcycle": "yes",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 709758407,
  "timestamp": "2019-08-01T18:50:06Z",
  "version": 1,
  "changeset": 72911454,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    445223320,
    5683580045,
    6671462008,
    5683580049
  ],
  "tags": {
    "name": "Ngõ 28",
    "hgv": "no",
    "highway": "residential",
    "maxweight": "1",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689227,
  "timestamp": "2019-04-19T04:43:23Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580043,
    5683580042,
    5683580041,
    5683580040,
    5683580039,
    5683580044,
    5683580038,
    4538570234
  ],
  "tags": {
    "name": "Ngõ 44",
    "motorcycle": "yes",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 596689233,
  "timestamp": "2019-04-19T04:43:24Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580054,
    5683580053,
    5683580052
  ],
  "tags": {
    "highway": "service"
  }
},
{
  "type": "way",
  "id": 616496953,
  "timestamp": "2019-04-19T04:43:24Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    4538570236,
    5828596775,
    5828596774
  ],
  "tags": {
    "name": "Ngõ 93",
    "motorcycle": "yes",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 675323607,
  "timestamp": "2019-04-19T04:43:23Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    445223320,
    6415482257,
    6415482256,
    4538570234,
    6415482254,
    4538570235
  ],
  "tags": {
    "name": "Phố Đại Linh",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 684700530,
  "timestamp": "2019-08-01T17:41:10Z",
  "version": 2,
  "changeset": 72909249,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    6415482254,
    6415482250,
    6415482252,
    6415482248,
    6415482244,
    6415482255,
    6415482237,
    6415482245
  ],
  "tags": {
    "name": "Ngõ 69",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 684702462,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 2,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580071,
    4538570239
  ],
  "tags": {
    "name": "Ngõ 127",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 684702463,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 2,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580070,
    5683580069
  ],
  "tags": {
    "name": "Ngõ 125",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 684702464,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 2,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    6415499210,
    6415499209
  ],
  "tags": {
    "name": "Ngõ 66",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689232,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 3,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580051,
    445223188
  ],
  "tags": {
    "name": "Ngõ 54",
    "highway": "residential",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689238,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 3,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580068,
    5683580062,
    5683580067
  ],
  "tags": {
    "name": "Ngõ 119",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 596689237,
  "timestamp": "2019-08-01T19:07:32Z",
  "version": 4,
  "changeset": 72912034,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580066,
    5683580065,
    5683580064,
    5683580059,
    6672087146,
    5683580063
  ],
  "tags": {
    "name": "Ngõ 97",
    "highway": "residential",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 596689239,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 4,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580071,
    6670677780,
    5683580070
  ],
  "tags": {
    "name": "Ngõ 127",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 402425921,
  "timestamp": "2019-07-31T16:06:34Z",
  "version": 10,
  "changeset": 72863792,
  "user": "ReedtheRiver",
  "uid": 9965337,
  "nodes": [
    445223386,
    6665925702,
    6415482251,
    5722094034,
    6415482249,
    445223320
  ],
  "tags": {
    "name": "Đại Linh",
    "highway": "tertiary",
    "lanes": "2",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 310168314,
  "timestamp": "2019-08-01T18:50:06Z",
  "version": 12,
  "changeset": 72911454,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    3155466740,
    5721894149,
    5721894147,
    5681231708,
    106068260,
    1720261338,
    282894611,
    3614460894,
    5681023545,
    5681023543,
    5683563830,
    5683563827,
    445223481
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Sa Đôi"
  }
},
{
  "type": "way",
  "id": 596689237,
  "timestamp": "2019-08-01T17:41:10Z",
  "version": 3,
  "changeset": 72909249,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580066,
    5683580065,
    5683580064,
    5683580059,
    5683580063
  ],
  "tags": {
    "name": "Ngõ 97",
    "highway": "residential",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 457756998,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 8,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4538570235,
    6668237460,
    5683580043,
    4538570236,
    5683580048,
    5683580050,
    5683580052,
    5683580051,
    5683580055,
    6415482253,
    4538570237,
    5683580057,
    5683580063,
    4538570238,
    5683580067,
    5683580069,
    6415499210,
    6670677782,
    6670677781,
    6668196043,
    4538570239
  ],
  "tags": {
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Đại Linh",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689237,
  "timestamp": "2019-08-01T17:41:10Z",
  "version": 3,
  "changeset": 72909249,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580066,
    5683580065,
    5683580064,
    5683580059,
    5683580063
  ],
  "tags": {
    "name": "Ngõ 97",
    "highway": "residential",
    "surface": "concrete"
  }
},
{
  "type": "way",
  "id": 457756998,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 8,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4538570235,
    6668237460,
    5683580043,
    4538570236,
    5683580048,
    5683580050,
    5683580052,
    5683580051,
    5683580055,
    6415482253,
    4538570237,
    5683580057,
    5683580063,
    4538570238,
    5683580067,
    5683580069,
    6415499210,
    6670677782,
    6670677781,
    6668196043,
    4538570239
  ],
  "tags": {
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Đại Linh",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596686701,
  "timestamp": "2018-06-12T01:15:23Z",
  "version": 1,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683563830,
    5683563825,
    5683563829
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 355926531,
  "timestamp": "2018-06-11T05:54:54Z",
  "version": 2,
  "changeset": 59728326,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    3614458992,
    5681023581,
    5681023532,
    3614460893,
    3614460894
  ],
  "tags": {
    "service": "driveway",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684700529,
  "timestamp": "2019-04-19T05:09:38Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    445223320,
    5683580045,
    5683580049,
    445223188,
    5683579498,
    5683579499,
    5683579516,
    4538570240
  ],
  "tags": {
    "highway": "residential",
    "name": "Ngõ 28"
  }
},
{
  "type": "way",
  "id": 310168314,
  "timestamp": "2019-07-26T18:29:32Z",
  "version": 11,
  "changeset": 72699677,
  "user": "daFisch",
  "uid": 8759590,
  "nodes": [
    3155466740,
    5721894149,
    5721894147,
    5681231708,
    106068260,
    1720261338,
    282894611,
    3614460894,
    5681023545,
    5681023543,
    5683563830,
    5683563827,
    445223481,
    5683563839,
    5683563843,
    4538571793,
    282894616
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Sa Đôi"
  }
},
{
  "type": "way",
  "id": 596686701,
  "timestamp": "2018-06-12T01:15:23Z",
  "version": 1,
  "changeset": 59757726,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683563830,
    5683563825,
    5683563829
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 355926531,
  "timestamp": "2018-06-11T05:54:54Z",
  "version": 2,
  "changeset": 59728326,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    3614458992,
    5681023581,
    5681023532,
    3614460893,
    3614460894
  ],
  "tags": {
    "service": "driveway",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684700529,
  "timestamp": "2019-04-19T05:09:38Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    445223320,
    5683580045,
    5683580049,
    445223188,
    5683579498,
    5683579499,
    5683579516,
    4538570240
  ],
  "tags": {
    "highway": "residential",
    "name": "Ngõ 28"
  }
},
{
  "type": "way",
  "id": 310168314,
  "timestamp": "2019-07-26T18:29:32Z",
  "version": 11,
  "changeset": 72699677,
  "user": "daFisch",
  "uid": 8759590,
  "nodes": [
    3155466740,
    5721894149,
    5721894147,
    5681231708,
    106068260,
    1720261338,
    282894611,
    3614460894,
    5681023545,
    5681023543,
    5683563830,
    5683563827,
    445223481,
    5683563839,
    5683563843,
    4538571793,
    282894616
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Sa Đôi"
  }
},
{
  "type": "way",
  "id": 684700530,
  "timestamp": "2019-04-19T04:43:22Z",
  "version": 1,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    6415482254,
    6415482250,
    6415482252,
    6415482248,
    6415482244,
    6415482255,
    6415482237,
    6415482245
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 69",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 596689237,
  "timestamp": "2019-04-19T04:43:23Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580066,
    5683580065,
    5683580064,
    5683580059,
    5683580063
  ],
  "tags": {
    "highway": "residential",
    "name": "Ngõ 97"
  }
},
{
  "type": "way",
  "id": 596689240,
  "timestamp": "2019-04-19T05:09:37Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580072,
    445223201
  ],
  "tags": {
    "name": "Ngõ 129",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596689231,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 3,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580050,
    5683580049
  ],
  "tags": {
    "motorcycle": "yes",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 684702465,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 3,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4538570240,
    445223285,
    4538570241,
    5683579508,
    445223342,
    5683580025,
    445223201,
    5683580032,
    5683580030,
    445223131,
    445223186,
    5683563824,
    5683563828,
    445223481
  ],
  "tags": {
    "name": "Phố Đại Linh",
    "highway": "tertiary",
    "lanes": "2",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 684700530,
  "timestamp": "2019-04-19T04:43:22Z",
  "version": 1,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    6415482254,
    6415482250,
    6415482252,
    6415482248,
    6415482244,
    6415482255,
    6415482237,
    6415482245
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 69",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 596689237,
  "timestamp": "2019-04-19T04:43:23Z",
  "version": 2,
  "changeset": 69364926,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580066,
    5683580065,
    5683580064,
    5683580059,
    5683580063
  ],
  "tags": {
    "highway": "residential",
    "name": "Ngõ 97"
  }
},
{
  "type": "way",
  "id": 596689240,
  "timestamp": "2019-04-19T05:09:37Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580072,
    445223201
  ],
  "tags": {
    "name": "Ngõ 129",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596689231,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 3,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580050,
    5683580049
  ],
  "tags": {
    "motorcycle": "yes",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 684702465,
  "timestamp": "2019-08-01T17:08:47Z",
  "version": 3,
  "changeset": 72908229,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4538570240,
    445223285,
    4538570241,
    5683579508,
    445223342,
    5683580025,
    445223201,
    5683580032,
    5683580030,
    445223131,
    445223186,
    5683563824,
    5683563828,
    445223481
  ],
  "tags": {
    "name": "Phố Đại Linh",
    "highway": "tertiary",
    "lanes": "2",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689234,
  "timestamp": "2018-06-12T01:34:23Z",
  "version": 1,
  "changeset": 59757887,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683580056,
    5683580055
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684702462,
  "timestamp": "2019-04-19T05:09:37Z",
  "version": 1,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580071,
    4538570239
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 127",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 684702463,
  "timestamp": "2019-04-19T05:09:37Z",
  "version": 1,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580070,
    5683580069
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 125",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 684702464,
  "timestamp": "2019-04-19T05:09:37Z",
  "version": 1,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    6415499210,
    6415499209
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 66",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 596689217,
  "timestamp": "2019-04-19T05:09:38Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    4538570239,
    4538570240
  ],
  "tags": {
    "motorcycle": "yes",
    "motor_vehicle": "no",
    "name": "Phố Đại Linh",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 596689238,
  "timestamp": "2019-04-19T05:09:38Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580068,
    5683580062,
    5683580067
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 119",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 596689241,
  "timestamp": "2019-04-19T05:09:39Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580081,
    5683580080,
    5683580079,
    5683580078,
    5683580077,
    5683580072,
    5683580076,
    5683580075,
    5683580074,
    5683580073,
    5683580071
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684702465,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 2,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4538570240,
    445223285,
    4538570241,
    5683579508,
    445223342,
    5683580025,
    445223201,
    5683580032,
    5683580030,
    445223131,
    445223186,
    5683563824,
    5683563828,
    445223481
  ],
  "tags": {
    "lanes": "2",
    "name": "Phố Đại Linh",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 596300522,
  "timestamp": "2019-04-19T05:09:39Z",
  "version": 3,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    282894611,
    5681047864,
    5681047863
  ],
  "tags": {
    "name": "Ngõ Chùa Đồng Bàn",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596689239,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 3,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580071,
    5683580070
  ],
  "tags": {
    "name": "Ngõ 127",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 457756998,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 7,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4538570235,
    6668237460,
    5683580043,
    4538570236,
    5683580048,
    5683580050,
    5683580052,
    5683580051,
    5683580055,
    6415482253,
    4538570237,
    5683580057,
    5683580063,
    4538570238,
    5683580067,
    5683580069,
    6415499210,
    6668196043,
    4538570239
  ],
  "tags": {
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Đại Linh",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596689234,
  "timestamp": "2018-06-12T01:34:23Z",
  "version": 1,
  "changeset": 59757887,
  "user": "surya8",
  "uid": 7671614,
  "nodes": [
    5683580056,
    5683580055
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684702462,
  "timestamp": "2019-04-19T05:09:37Z",
  "version": 1,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580071,
    4538570239
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 127",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 684702463,
  "timestamp": "2019-04-19T05:09:37Z",
  "version": 1,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580070,
    5683580069
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 125",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 684702464,
  "timestamp": "2019-04-19T05:09:37Z",
  "version": 1,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    6415499210,
    6415499209
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 66",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 596689217,
  "timestamp": "2019-04-19T05:09:38Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    4538570239,
    4538570240
  ],
  "tags": {
    "motorcycle": "yes",
    "motor_vehicle": "no",
    "name": "Phố Đại Linh",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 596689238,
  "timestamp": "2019-04-19T05:09:38Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580068,
    5683580062,
    5683580067
  ],
  "tags": {
    "motorcycle": "yes",
    "name": "Ngõ 119",
    "highway": "residential",
    "motor_vehicle": "no"
  }
},
{
  "type": "way",
  "id": 596689241,
  "timestamp": "2019-04-19T05:09:39Z",
  "version": 2,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    5683580081,
    5683580080,
    5683580079,
    5683580078,
    5683580077,
    5683580072,
    5683580076,
    5683580075,
    5683580074,
    5683580073,
    5683580071
  ],
  "tags": {
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 684702465,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 2,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4538570240,
    445223285,
    4538570241,
    5683579508,
    445223342,
    5683580025,
    445223201,
    5683580032,
    5683580030,
    445223131,
    445223186,
    5683563824,
    5683563828,
    445223481
  ],
  "tags": {
    "lanes": "2",
    "name": "Phố Đại Linh",
    "highway": "tertiary"
  }
},
{
  "type": "way",
  "id": 596300522,
  "timestamp": "2019-04-19T05:09:39Z",
  "version": 3,
  "changeset": 69365209,
  "user": "Corban8",
  "uid": 4240913,
  "nodes": [
    282894611,
    5681047864,
    5681047863
  ],
  "tags": {
    "name": "Ngõ Chùa Đồng Bàn",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596689239,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 3,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5683580071,
    5683580070
  ],
  "tags": {
    "name": "Ngõ 127",
    "highway": "residential",
    "motor_vehicle": "no",
    "motorcycle": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 457756998,
  "timestamp": "2019-07-31T22:59:29Z",
  "version": 7,
  "changeset": 72875181,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4538570235,
    6668237460,
    5683580043,
    4538570236,
    5683580048,
    5683580050,
    5683580052,
    5683580051,
    5683580055,
    6415482253,
    4538570237,
    5683580057,
    5683580063,
    4538570238,
    5683580067,
    5683580069,
    6415499210,
    6668196043,
    4538570239
  ],
  "tags": {
    "highway": "tertiary",
    "lanes": "2",
    "name": "Phố Đại Linh",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 596785317,
  "timestamp": "2019-07-31T16:54:50Z",
  "version": 3,
  "changeset": 72865615,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5684223055,
    5684223053
  ],
  "tags": {
    "highway": "residential",
    "oneway": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 597139537,
  "timestamp": "2019-08-01T12:28:45Z",
  "version": 3,
  "changeset": 72896443,
  "user": "spuddy93",
  "uid": 8600365,
  "nodes": [
    5684223057,
    5686582028,
    5686582027,
    4084101415
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 596785320,
  "timestamp": "2019-07-30T20:12:30Z",
  "version": 4,
  "changeset": 72828767,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5684223053,
    6662386041,
    6662386040,
    5684223057
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 597232543,
  "timestamp": "2019-07-31T20:54:51Z",
  "version": 4,
  "changeset": 72872829,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5687161283,
    6668094822,
    5687161284,
    5697944076,
    5684223056
  ],
  "tags": {
    "highway": "residential",
    "oneway": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 708940568,
  "timestamp": "2019-07-31T16:19:02Z",
  "version": 4,
  "changeset": 72864281,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4084101437,
    6662274274,
    6662274275,
    6666358851,
    6662274276,
    6662274277,
    6441639134,
    5686529993,
    6662274278,
    6662274280,
    5686529987,
    6662274281,
    6662274279,
    6661539015,
    4084101374
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "maxspeed": "20"
  }
},
{
  "type": "way",
  "id": 596714950,
  "timestamp": "2019-08-01T12:28:45Z",
  "version": 5,
  "changeset": 72896443,
  "user": "spuddy93",
  "uid": 8600365,
  "nodes": [
    5684365037,
    5684364986,
    5684364994,
    5684364985,
    5683736891,
    6667972292,
    5683736836,
    5683736886,
    5683736888,
    5683736892
  ],
  "tags": {
    "surface": "concrete",
    "highway": "residential",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 596714951,
  "timestamp": "2019-08-01T12:28:45Z",
  "version": 5,
  "changeset": 72896443,
  "user": "spuddy93",
  "uid": 8600365,
  "nodes": [
    5683736894,
    5683736889,
    5683736853,
    6647589358,
    5683736893,
    5684364990,
    5684364988,
    5684365025
  ],
  "tags": {
    "surface": "concrete",
    "highway": "residential",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 597139536,
  "timestamp": "2019-07-31T20:09:55Z",
  "version": 5,
  "changeset": 72871676,
  "user": "ReedtheRiver",
  "uid": 9965337,
  "nodes": [
    4084101415,
    6662386038,
    5686582030,
    6662386037,
    5686582031,
    6662386035,
    4084101381,
    6666507325,
    5686580417,
    5686580420
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "maxspeed": "20",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 406325446,
  "timestamp": "2019-07-31T20:54:51Z",
  "version": 11,
  "changeset": 72872829,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4084101396,
    6661768499,
    6668094824,
    6668059396,
    5686529991,
    6668059399,
    6666358849,
    4084101437,
    6662274273,
    6662274271,
    5684365028,
    4084101465,
    5684365029,
    6662386044,
    4084101480,
    6666507330,
    5684223053
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "maxspeed": "20",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 406325319,
  "timestamp": "2019-08-01T00:20:33Z",
  "version": 18,
  "changeset": 72876232,
  "user": "spuddy93",
  "uid": 8600365,
  "nodes": [
    4084101309,
    4084101312,
    6661768503,
    6659214325,
    6659214328,
    5686529947,
    6659214326,
    6659214331,
    5686529980,
    6659214333,
    6659214336,
    5686529974,
    6659214338,
    6661623758,
    6661623757,
    4084101354,
    5686530004,
    6658820390,
    6658820389,
    5686529985,
    6659211858,
    6659211859,
    5686530008,
    6659211860,
    6659211861,
    5686530017,
    6659211857,
    6659211862,
    5686530010,
    6659211856,
    6659211863,
    5686530016,
    4084101396,
    5684365032,
    4084101402,
    5684364981,
    4084101485,
    5684364982,
    4084101496,
    5684364976,
    4084101502,
    4084101512
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential"
  }
},
{
  "type": "way",
  "id": 596785317,
  "timestamp": "2019-07-31T16:54:50Z",
  "version": 3,
  "changeset": 72865615,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5684223055,
    5684223053
  ],
  "tags": {
    "highway": "residential",
    "oneway": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 597139537,
  "timestamp": "2019-08-01T12:28:45Z",
  "version": 3,
  "changeset": 72896443,
  "user": "spuddy93",
  "uid": 8600365,
  "nodes": [
    5684223057,
    5686582028,
    5686582027,
    4084101415
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 596785320,
  "timestamp": "2019-07-30T20:12:30Z",
  "version": 4,
  "changeset": 72828767,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5684223053,
    6662386041,
    6662386040,
    5684223057
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 597232543,
  "timestamp": "2019-07-31T20:54:51Z",
  "version": 4,
  "changeset": 72872829,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    5687161283,
    6668094822,
    5687161284,
    5697944076,
    5684223056
  ],
  "tags": {
    "highway": "residential",
    "oneway": "yes",
    "surface": "asphalt"
  }
},
{
  "type": "way",
  "id": 708940568,
  "timestamp": "2019-07-31T16:19:02Z",
  "version": 4,
  "changeset": 72864281,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4084101437,
    6662274274,
    6662274275,
    6666358851,
    6662274276,
    6662274277,
    6441639134,
    5686529993,
    6662274278,
    6662274280,
    5686529987,
    6662274281,
    6662274279,
    6661539015,
    4084101374
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "maxspeed": "20"
  }
},
{
  "type": "way",
  "id": 596714950,
  "timestamp": "2019-08-01T12:28:45Z",
  "version": 5,
  "changeset": 72896443,
  "user": "spuddy93",
  "uid": 8600365,
  "nodes": [
    5684365037,
    5684364986,
    5684364994,
    5684364985,
    5683736891,
    6667972292,
    5683736836,
    5683736886,
    5683736888,
    5683736892
  ],
  "tags": {
    "surface": "concrete",
    "highway": "residential",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 596714951,
  "timestamp": "2019-08-01T12:28:45Z",
  "version": 5,
  "changeset": 72896443,
  "user": "spuddy93",
  "uid": 8600365,
  "nodes": [
    5683736894,
    5683736889,
    5683736853,
    6647589358,
    5683736893,
    5684364990,
    5684364988,
    5684365025
  ],
  "tags": {
    "surface": "concrete",
    "highway": "residential",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 597139536,
  "timestamp": "2019-07-31T20:09:55Z",
  "version": 5,
  "changeset": 72871676,
  "user": "ReedtheRiver",
  "uid": 9965337,
  "nodes": [
    4084101415,
    6662386038,
    5686582030,
    6662386037,
    5686582031,
    6662386035,
    4084101381,
    6666507325,
    5686580417,
    5686580420
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "maxspeed": "20",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 406325446,
  "timestamp": "2019-07-31T20:54:51Z",
  "version": 11,
  "changeset": 72872829,
  "user": "Traaker_L",
  "uid": 9320902,
  "nodes": [
    4084101396,
    6661768499,
    6668094824,
    6668059396,
    5686529991,
    6668059399,
    6666358849,
    4084101437,
    6662274273,
    6662274271,
    5684365028,
    4084101465,
    5684365029,
    6662386044,
    4084101480,
    6666507330,
    5684223053
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential",
    "maxspeed": "20",
    "oneway": "yes"
  }
},
{
  "type": "way",
  "id": 406325319,
  "timestamp": "2019-08-01T00:20:33Z",
  "version": 18,
  "changeset": 72876232,
  "user": "spuddy93",
  "uid": 8600365,
  "nodes": [
    4084101309,
    4084101312,
    6661768503,
    6659214325,
    6659214328,
    5686529947,
    6659214326,
    6659214331,
    5686529980,
    6659214333,
    6659214336,
    5686529974,
    6659214338,
    6661623758,
    6661623757,
    4084101354,
    5686530004,
    6658820390,
    6658820389,
    5686529985,
    6659211858,
    6659211859,
    5686530008,
    6659211860,
    6659211861,
    5686530017,
    6659211857,
    6659211862,
    5686530010,
    6659211856,
    6659211863,
    5686530016,
    4084101396,
    5684365032,
    4084101402,
    5684364981,
    4084101485,
    5684364982,
    4084101496,
    5684364976,
    4084101502,
    4084101512
  ],
  "tags": {
    "surface": "asphalt",
    "highway": "residential"
  }
}

  ]
}





def count_tag_change(changesets,info_json,osm_obj_type='*'):
    #print(info_json)
    tags_to_check = info_json['tags']
    #for tag in tags_to_check:
        #print(tag)

    #def count_tag_change(changesets,tags, osm_obj_type="*",const_tag="none"):
    #Testing variables
    print_version_lists = False
    object_limit_for_query=0
    print_query = False
    dont_run_query = True
    use_hardcoded_query_result = True
    print_query_response = False
    dont_process_query = False
    #TODO: sort data of tag changes by changeset, then by tag for column data in csv
    #changesets = {<changeset_id>:{<tag_to_check>:[<objects>]}}
    objects_by_changeset = {}
    #new_ver_objects = []

    #Get all objects touched in each changeset
    #We go by changeset, then by tag
    for changeset in changesets:
        #New changeset in list
        objects_by_changeset[changeset] = {} #?
        #Request XML for each changeset
        api_url = "https://www.openstreetmap.org/api/0.6/changeset/{changeset}/download".format(changeset=changeset)
        dev_api_url = "https://master.apis.dev.openstreetmap.org/api/0.6/changeset/{changeset}/download".format(changeset=changeset)
        #api_url = api_url
        session = CacheControl(requests.session())
        result = session.get(api_url).text
        root = ET.fromstring(result)

        #If we are looking for a constant tag
        for this_tag in tags_to_check:
            check_tag = this_tag['tag']
            #print('check_tag: ',check_tag)

            const_tag = this_tag['const']
            #print('const_tag: ', const_tag)
            objects_by_changeset[changeset][check_tag+'_'+const_tag] = []

            if const_tag != "none":
                #print('checking for const ',const_tag)
                #Retrieve all objects that have the tags we're looking for
                objs_modified = root.findall("./modify/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
                objs_created = root.findall("./create/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))
                objs_deleted = root.findall("./delete/{osm_obj_type}/tag[@k='{const_tag}']..".format(const_tag=const_tag,osm_obj_type=osm_obj_type))

                #Store each modified object's data in our list, new_ver_objects, as dictionaries
                for obj in objs_modified:
                    this_obj = {"id":obj.attrib['id'],"version":int(obj.attrib['version'])}
                    tag_elements = obj.findall("tag")
                    for tag_element in tag_elements:
                        this_obj[tag_element.attrib['k']] = tag_element.attrib['v']
                    #print(check_tag)
                    objects_by_changeset[changeset][check_tag+'_'+const_tag].append(this_obj)

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
                    for tag_element in tag_elements:
                        this_obj[tag_element.attrib['k']] = tag_element.attrib['v']


                    objects_by_changeset[changeset][check_tag+'_'+const_tag].append(this_obj)


    change_count_by_changeset = {}
    #print(objects_by_changeset)

    #Count number of objects per changeset
    for set in objects_by_changeset:
        change_count_by_changeset[set] = {}
        for tag in objects_by_changeset[set]:
            change_count_by_changeset[set][tag] = len(objects_by_changeset[set][tag])

    #print('counts: ')
    #print(change_count_by_changeset)

    #for set in change_count_by_changeset:
        #print(change_count_by_changeset[set])








    #4Testing: print objects and data in new_ver_objects list
    if print_version_lists:
        print("New_Ver: ")
        print(objects_by_changeset)
        print()

    #Build query to get previous versions of all objects in new_ver_objects
   #Start of Overpass Query
   #We will go by changeset, then by tag
   #[<changeset>][<tag>]
    query = "[out:json][timeout:25];"
    query_count = 0
    for this_set in objects_by_changeset:
        for this_tag in objects_by_changeset[this_set]:
            #Build each query part for each object
            if (query_count < object_limit_for_query or object_limit_for_query == 0):
                for obj in objects_by_changeset[this_set][this_tag]:
                    #print(obj)
                    #>>>Prints dictionary of object{'id':<value>,'version':<value>,<keys and values for each tag afterwards}
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
    if print_query:
        print('Query: ')
        print(query)

    if dont_run_query == False:
        #Submit the query
        query_json = overpass_query(query)

    if print_query_response:
        if dont_run_query:
            print("Cannot print query response if it was not run")
        else:
            print(query_json)


    if (dont_process_query == False and dont_run_query == False)\
    or use_hardcoded_query_result:
        #4Testing: use a canned query_result from a string
        if use_hardcoded_query_result:
            query_json = HARDCODED_QUERY_RESULT
        #Dictionaries of id, value, version
        old_ver_objects = []
        old_objects_by_changeset = {}
        #old_objects_by_changeset{<changeset_id>:{<tag_to_check>:[<objects>]}}
        #We go by changeset, then tag
        #We will index tags inside of indexing changesets
        current_set_index = 0
        current_tag_index = 0
        #print('we gotta figure out which to use: ',tags_to_check)
        #>> [{'tag': 'name', 'const': 'highway'}, {'tag': 'name', 'const': 'waterway'}]
        #old_objects_by_changeset[<changeset_id>][tags_to_check[index]['tag']]
        #old_objects_by_changeset[changesets[current_set_index]][tag].append(this_obj)
        #obj_by_changeset anatomy: {<change_id>:{<tag_const>:[<list of values>],<tag_const:[<list of values>]}}
        objects_added = 0

        old_objects_by_changeset={}

        #Iterate through query result elements
        old_version_objects = []
        for element in query_json["elements"]:
            this_obj = this_obj = {"id":element['id'],"version":element['version']}
            for key, value in element['tags'].items():
                this_obj[key] = value
            old_version_objects.append(this_obj)
            #these_tags = element['tags']

        #Sort list of objects by changeset and tag
        #print('Objects to be sorted')
        old_obj_index = 0
        for set in objects_by_changeset:
            old_objects_by_changeset[set] = {}
            #print(set)
            #>>> outputs all changeset ids repeatedly?
            objects_by_tag = objects_by_changeset[set]
            for tag in objects_by_tag:

                #print('For Tag: ',tag)

                old_objects_by_changeset[set][tag] = []
                #print(tag)
                #>>> alternating 'name_highway'\n'name_waterway'\n
                #old_objects_by_changeset[changesets[current_set_index]][tag]
                #objects_by_tag[tag] gives us the list of objects that we need to check
                #We can iterate through this list to get the objects
                for this_obj in objects_by_tag[tag]:
                    #Iterate through tags in the query response json
                    #print(old_obj_index)
                    if old_obj_index < object_limit_for_query or object_limit_for_query == 0:
                        obj_to_add = old_version_objects[old_obj_index]
                        old_obj_index += 1
                        #print(obj_to_add)
                        old_objects_by_changeset[set][tag].append(obj_to_add)

                        #print(obj_to_add)


                    #print(this_obj)
                    #Prints the dict containing the object id, the version, and all tags
            #print()



            '''
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
            '''

        #4Testing: Print list of old-version objects
        if print_version_lists:
            print("Old_Ver: ")
            print(old_objects_by_changeset)
            print()

        #See what values changed
        changes_by_changeset = {}
        #Initialize change counts for all sets
        for this_changeset in old_objects_by_changeset:
            #print(this_changeset)
            #>>> changeset id
            changes_by_changeset[this_changeset] = {}
            for this_tag in old_objects_by_changeset[this_changeset]:
                #print(this_tag)
                #tag + '_' + const_tag e.g. name_highway
                add_key = this_tag +' added'
                modify_key = this_tag + ' modified'
                print(modify_key)
                delete_key = this_tag + ' deleted'
                changes_by_changeset[this_changeset][this_tag] = {add_key:0,modify_key:0,delete_key:0}



        '''
        for tag in tags_to_check:
            print(tag)
            for set, changes in old_objects_by_changeset.items():
                changes_by_changeset[set] = {'added':0,'modified':0,'deleted':0}
        '''

        differences_counted = 0
        compare_index = 0
        tag_index = 0
        #print("Full print of old")
        for this_changeset in old_objects_by_changeset:
            #print('1')
            tag_index = 0
            for this_tag in old_objects_by_changeset[this_changeset]:
                #print('2')
                #tag + '_' + const_tag e.g. name_highway
                compare_index = 0
                for this_obj in old_objects_by_changeset[this_changeset][this_tag]:
                    #print('3')
                    this_tag_to_check = tags_to_check[tag_index]['tag']

                    old_obj = old_objects_by_changeset[this_changeset][this_tag][compare_index]
                    new_obj = objects_by_changeset[this_changeset][this_tag][compare_index]

                    #print(old_obj['id'],": ",new_obj['id'])
                    if str(old_obj['id']) != new_obj['id']:
                        print('ERROR: ID MISTMATCH')

                    old_val = None
                    if old_obj.get(this_tag_to_check,False):
                        old_val = old_obj[this_tag_to_check]

                    new_val = None
                    if new_obj.get(this_tag_to_check,False):
                        new_val = new_obj[this_tag_to_check]

                    if old_val == None:
                        if new_val != None:
                            if old_val != new_val:
                                print(new_val,' added')
                                changes_by_changeset[this_changeset][this_tag][this_tag +' added'] += 1
                                #changes_by_changeset[set]['added'] += 1
                            else:
                                print(old_val," didn't change")
                    else:
                        if new_val != None:
                            if old_val != new_val:
                                print(old_val,' changed to ',new_val)
                                changes_by_changeset[this_changeset][this_tag][this_tag +' modified'] += 1
                                #changes_by_changeset[set]['modified'] += 1
                            else:
                                print(old_val," didn't change")
                        else:
                            if old_val != new_val:
                                print(old_val,' deleted')
                                changes_by_changeset[this_changeset][this_tag][this_tag +' deleted'] += 1
                                #changes_by_changeset[set]['deleted'] += 1
                            else:
                                print(old_val," didn't change")




                    compare_index += 1

                tag_index += 1

        print(differences_counted, "WOO")
        print(changes_by_changeset)

        '''
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
            '''
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


#print(\
count_tag_change([72917146,72916726,72916312,72915002,72913700,72912034,72911454,72909249,72908229,72905720],TEST_JSON_DICT,"way")\
#)
