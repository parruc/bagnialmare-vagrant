#!/usr/bin/env python

import sys
import geopy
import simplejson

filename = sys.argv[1]
gc = geopy.geocoders.GoogleV3(domain='maps.google.it')
with open(filename, "r") as f:
    bagni = simplejson.load(f)
for b in bagni:
    if not 'coords' in b:
        if 'address' in b:
            place = b['address'] + ', ' + b['city']
            try:
                coords = list(gc.geocode(place, region="it")[1]) 
	        print place, coords
	        b['coords'] = coords
            except:
                print "cannot find coords"
                print place, coords
with open(filename, "w") as output:
    simplejson.dump(bangi, output)    
        
