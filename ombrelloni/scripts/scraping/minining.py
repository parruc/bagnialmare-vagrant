#!/usr/bin/env python

import os
import simplejson
import re
from django.core.validators import email_re

hotel_re = re.compile("(hotel)|(albergo)|(pensione)|(residence)|(camping)|(campeggio)", flags=re.I)
json_filenames = [f for f in os.listdir(".") if f.startswith("output")]
bagni = []
for filename in json_filenames:
    with open(filename, "r") as f:
        bagni.extend(simplejson.load(f))
numero_bagni = len(bagni)
print "totale bagni estratti:\t%d" % (numero_bagni,)
nomi_bagni = set([b['name'] for b in bagni])
print "totale nomi unici:\t%d" % (len(nomi_bagni),)
email_bagni = set([b['mail'] for b in bagni if 'mail' in b])
print "totale indirizzi mail unici:\t%d" % (len(email_bagni),)
email_bagni_valide = set([m for m in email_bagni if email_re.search(m)])
print "totale indirizzi mail validi:\t%d" % (len(email_bagni_valide),)
email_bagni_hotel = set([m for m in email_bagni_valide if hotel_re.search(m)])
print "totale indirizzi mail hotel:\t%d" % (len(email_bagni_hotel),)
siti_hotel = [b['site'] for b in bagni if 'site' in b]
print "totale bagni con sito internet:\t%d" % (len(siti_hotel),)
coords_bagni = [b['coords'] for b in bagni if 'coords' in b]
print "totale bagni con coordinate:\t%d" % (len(coords_bagni),)

