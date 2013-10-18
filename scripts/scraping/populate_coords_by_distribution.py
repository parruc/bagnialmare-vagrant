#!/usr/bin/env python

import os
import json

#data related to pinarella
#city = 'Pinarella'
#location_unit_latitude, location_unit_longitude = 0.000182667, 0.000118597
#location_origin_latitude, location_origin_longitude = 44.233331, 12.376825
#location_first_bagno_number = 59
#filename = 'output_cervia.json'

#data related to Cervia
#city = 'Cervia'
#location_unit_latitude, location_unit_longitude = 0.000206095, 0.000105841
#location_origin_latitude, location_origin_longitude = 44.24885, 12.366655
#location_first_bagno_number = 146
#filename = 'output_cervia.json'

#data related to Milano (fucking) Marittima
#city = 'Milano Marittima'
#location_unit_latitude, location_unit_longitude = 0.0002992, 0.000093867
#location_origin_latitude, location_origin_longitude = 44.26848, 12.357242
#location_first_bagno_number = 235
#filename = 'output_cervia.json'

#data related to Tagliata
#city = 'Tagliata'
#location_unit_latitude, location_unit_longitude = 0.00017766, 0.00014272
#location_origin_latitude, location_origin_longitude = 44.224659, 12.383318
#location_first_bagno_number = 3
#filename = 'output_cervia.json'

#data related to Riccione
city = 'Riccione'
location_unit_latitude, location_unit_longitude = 0.00025000, 0.00037370
location_origin_latitude, location_origin_longitude = 43.986385, 12.688859  
location_first_bagno_number = 1
filename = 'output_riccione.json'

def get_coords(bagno_number, first_bagno_number, unit_latitude, unit_longitude, origin_latitude, origin_longitude):
    relative_bagno_number = bagno_number - first_bagno_number
    latitude = origin_latitude + (relative_bagno_number * unit_latitude) 
    longitude = origin_longitude - (relative_bagno_number * unit_longitude)
    return latitude, longitude

def get_bagno_number(bagno):
    if 'number' not in bagno:
        raise Exception('Bagno without number: %s - %s' % (bagno['name'], bagno['address']))
    number = bagno['number']
    if number.isdigit():
        number = number
    elif '-' in number: # 49-50
        number = number[:number.find('-')].strip()
    elif '/' in number: # 127/128
        number = number[:number.find('/')].strip()
    elif 'bis' in number:  # 127 bis
        number = number[:number.find('bis')].strip()
    else:
        raise Exception('Unknow bagno number format: ' + number)
    return int(number)

json_filenames = [f for f in os.listdir(".") if f.startswith(filename)]
locations = {}
bagni = []
coords_list = []
for filename in json_filenames:
    with open(filename, "r") as f:
        bagni.extend(json.load(f))

for bagno in bagni:
    if bagno['city'] == city:
        number = get_bagno_number(bagno)
        latitude, longitude = get_coords(number, location_first_bagno_number, location_unit_latitude, location_unit_longitude, 
                                                                    location_origin_latitude, location_origin_longitude)
        bagno['coords'] = [str(latitude), str(longitude)]


print json.dumps(bagni, sort_keys=True, indent=4)

