#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import urllib.request
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f','--from', help='Departure station', required=True)
parser.add_argument('-t','--to', help='Arrival station', required=True)
parser.add_argument('-c','--time', help='Departure time', required=False)

args = vars(parser.parse_args())

url = 'http://transport.opendata.ch/v1/connections?from=' + str(args['from'].replace(' ','%20').encode('utf-8')) + '&to=' + str(args['to'].replace(' ','%20').encode('utf-8')) + '&fields[]=connections/from&fields[]=connections/to&fields[]=connections/duration&limit=6&time=' + str(args['time'].replace(' ','%20').encode('utf-8'))

try: response = urllib.request.urlopen(url)
except urllib.error.URLError as e:
    print("Network error! " + str(e))
else:
    data = response.read()# a `bytes` object
    text = data.decode('utf-8')

    data = json.loads(text)

    if data['connections']:
        conn = [0] * 6

        for i in range(0,6):
            conn[0] = data['connections'][i]['from']['station']['name']
            conn[1] = data['connections'][i]['to']['station']['name']
            conn[2] = data['connections'][i]['from']['departure']
            conn[3] = data['connections'][i]['to']['arrival']
            conn[4] = data['connections'][i]['duration']

            print("[" + str(i+1) + "] From: " + conn[0] + " At: " + conn[2][11:16] + " To: " + conn[1] + " At: " + conn[3][11:16] + " Duration: " + conn[4][4:12])
    else:
        print("Not found!")
