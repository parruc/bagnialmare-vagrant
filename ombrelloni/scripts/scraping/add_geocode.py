#!/usr/bin/env python

import geopy
import logging

def coords_from_address(addr, region="it"):
    coords = None
    try:
        coords = list(gc.geocode(addr, region)[1])
    except:
        logging.error("cannot find: " + addr)
        raise
    return coords

if __name__ == "__main__":
    import argparse
    import simplejson
    logger = logging.getLogger("coord patch")
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="patch json file with coords")
    parser.add_argument("filename",
                        nargs = '+',
                        help="filename, json data to be patched")
    args = parser.parse_args()
    bagni = []
    added = 0 
    not_found = 0
    gc = geopy.geocoders.GoogleV3(domain='maps.google.it')
    for filename in args.filename:
        logger.info("analyze data from: %s" % (filename,))
        with open(filename, "r") as f:
            _bagni = simplejson.load(f)
        for b in _bagni:
            if (not 'coords' in b and
            'address' in b and 
            'city' in b):
                coords = coords_from_address(b['address'] + ', ' +
                                             b['city'])
                if coords:
                    b['coords'] = coords
                    added += 1
                else:
                    not_found += 1
        bagni.extend(_bagni)
    outfilename = "bagni.json"
    logger.info("write output to: %s" % (outfilename,))
    logger.info("added %d coords" % (added,))
    logger.info("not found %d coords" % (not_found,))
    bagni.sort(key=lambda x:x['name'])
    with open(outfilename, "w") as output:
        simplejson.dump(bagni, output)    

        
