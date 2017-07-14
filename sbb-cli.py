#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.parse
import urllib.request
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--from', help='Departure station', required=True)
parser.add_argument('-t', '--to', help='Arrival station', required=True)
parser.add_argument('-c', '--time', help='Departure time', required=False)
parser.add_argument('-d', '--detail', help='Verbose output', required=False)

args = vars(parser.parse_args())

if args['detail']:
    url = 'http://transport.opendata.ch/v1/connections?from=' + str(args['from'].replace(' ','%20').encode('utf-8')) \
        + '&to=' + str(args['to'].replace(' ','%20').encode('utf-8')) + '&limit=6'
else:
    url = 'http://transport.opendata.ch/v1/connections?from=' + str(args['from'].replace(' ','%20').encode('utf-8')) \
        + '&to=' + str(args['to'].replace(' ','%20').encode('utf-8')) + '&fields[]=connections/from&fields[]=connections/to&fields[]=connections/duration&limit=6'

if args['time']:
    url = url + '&time=' + urllib.parse.quote_plus(str(args['time'].replace(' ','%20')))

try: response = urllib.request.urlopen(url)
except urllib.error.URLError as e:
    print("Network error! " + str(e))
else:
    data = response.read()# a `bytes` object
    text = data.decode('utf-8')

    data = json.loads(text)

    if data['connections']:
        conn = [0] * 6

        index = 0
        for i in data['connections']:
            index = index + 1

            print("[" + str(index) + "] From: " + i['from']['station']['name']
                + " (" + (i['from']['platform'] or "-") + ")" + " At: " + i['from']['departure'][11:16]
                    + " To: " + i['to']['station']['name'] + " At: " + i['to']['arrival'][11:16] + " Duration: " + i['duration'][4:12])

        if args['detail']:
            if data['connections']:

                print("\nConnection: " + str(int(args['detail'])) + ":")
                for i in data['connections'][int(args['detail'])-1]['sections']:
                    journeyDetail = i['journey']
                    departureDetail = i['departure']
                    arrivalDetail = i['arrival']
                    if journeyDetail:
                        print("Station: " + departureDetail['station']['name'] + " At: " + departureDetail['departure'][11:16]
                            + " Platform: (" + departureDetail['platform'] +  ") \"" + str(journeyDetail['name'])
                                + "\" Heading to: " + journeyDetail['to'] )
            else:
                print("Details not found!")

    else:
        print("Not found!")
