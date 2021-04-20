#!/usr/bin/env python3
# -*- coding: utf-8 -*-
DEBUG=False
JSONDEBUG=False

import json
import urllib.parse
import urllib.request
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--from', help='Departure station', required=True)
parser.add_argument('-t', '--to', help='Arrival station', required=True)
parser.add_argument('-c', '--time', help='Departure time', required=False)
#parser.add_argument('-v', '--via', help='Via station ', required=False)
# TODO: add vias
parser.add_argument('-d', '--detail', help='Verbose output', required=False)
args = vars(parser.parse_args())

def request_json(url):
    DEBUG and print(url)
    try: response = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("Network error! " + str(e))
    else:
        data = response.read()# a `bytes` object
        text = data.decode('utf-8')
        j = json.loads(text)
        JSONDEBUG and json.dumps(j,indent=4)
        return j

# In the next paragraph we get the "closest" station from the provided string.
# Note this (should) coincides with the first item from the suggestion list
# from the web interface of SBB
# Doing this allows for example to type Zürich instead of Zürich HB
# This additionally allows for addresses to be resolved to a nearby station.
# Doc: http://transport.opendata.ch/docs.html#connections
station = {}
station['from'] = str(args['from'])
station['to'] = str(args['to'])
#station['via1'] = str(args['via'].replace(' ','%20').encode('utf-8'))
for s in station:
    url = 'http://transport.opendata.ch/v1/locations?query=' \
        + urllib.parse.quote(station[s]) \
        + '&fields[]=stations/name'
    # TODO: check for the "refine" type of a station
    data = request_json(url)
    if data['stations']:
        stations = data['stations']
        # the following block just selects the first id of all returend 
        # stations
        if len(stations) > 0 and stations[0]['name']:
            DEBUG and print(stations[0]['name'])
            station[s] = stations[0]['name']
    else:
        print('No station found corresponding to ' + station[s] + '!')

# This paragraph gets the connection form the determined stations
if args['detail']:
    url = 'http://transport.opendata.ch/v1/connections?from=' \
        + urllib.parse.quote(str(station['from'])) + '&to=' \
        + urllib.parse.quote(str(station['to'])) + '&limit=6'
else:
    url = 'http://transport.opendata.ch/v1/connections?from=' \
        + urllib.parse.quote(str(station['from'])) + '&to=' \
        + urllib.parse.quote(str(station['to']))\
        + '&fields[]=connections/from&fields[]=connections/to&fields[]=connections/duration&limit=6'

if args['time']:
    url = url + '&time=' + urllib.parse.quote_plus(str(args['time'].replace(' ','%20')))

data = request_json(url)
if data['connections']:
    index = 0
    for i in data['connections']:
        index = index + 1

        print("[" + str(index) + "] From: " + i['from']['station']['name']
            + " (" + (i['from']['platform'] or "-") + ")" + " At: " + i['from']['departure'][11:16]
                + " To: " + i['to']['station']['name'] + " At: " + i['to']['arrival'][11:16] + " Duration: " + i['duration'][4:12])

    if args['detail']:
        if data['connections']:

            print("\nConnection [" + str(int(args['detail'])) + "]:")
            for i in data['connections'][int(args['detail'])-1]['sections']:

                if i['journey']:
                    print("Station: " + i['departure']['station']['name'] + " At: " + i['departure']['departure'][11:16]
                        + " Platform: (" + (i['departure']['platform'] or "-") +  ") \"" + str(i['journey']['name'])
                            + "\" Heading to: " + i['journey']['to'] )
                            #i['arrival']
        else:
            print("Details not found!")

else:
    print("Not found!")


