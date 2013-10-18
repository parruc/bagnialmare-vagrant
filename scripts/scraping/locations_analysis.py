#!/usr/bin/env python

import os
import json

json_filenames = [f for f in os.listdir(".") if f.startswith("output_ricci")]
locations = {}
bagni_with_number = 0
bagni = []
for filename in json_filenames:
    with open(filename, "r") as f:
        bagni.extend(json.load(f))

print len(bagni)

for bagno in bagni:
    bagni_with_number = bagni_with_number + 1 if bagno.has_key('number') else bagni_with_number
    city = bagno['city'] if bagno.has_key('city') else 'no_city'
    locations[city] = locations[city] + 1 if locations.has_key(city) else 1

#locations = set([bagno['city'] if bagno.has_key('city') else 'no_city' for bagno in bagni])
for location in locations:
    print location, locations[location]

print bagni_with_number

#print "totale bagni estratti:\t%d" % (numero_bagni,)
#nomi_bagni = set([b['name'] for b in bagni])

