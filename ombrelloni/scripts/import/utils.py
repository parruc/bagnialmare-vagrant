# -*- coding: utf-8 -*-
import urllib2
import socket
import logging
import time
import types
import json

TIMEOUT = 5
MAX_RETRIES = 3
SLEEPTIME = 5

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")]

def read_aliases():
    try:
        with open('aliases.json', 'r') as aliases_file:
            return json.load(aliases_file)
    except IOError:
        return []

def get_service_from_alias(service_name):
    service_list = [service_name, ]
    ALIASES = read_aliases()
    if service_name in ALIASES:
        service_list = ALIASES[service_name]
        if isinstance(service_list, types.StringTypes):
            service_list = [service_list, ]
    return service_list

def read_services():
    try:
        with open('services.json', 'r') as services_file:
            return json.load(services_file)
    except IOError:
        return []

def write_services(services):
    with open('services.json', 'a') as services_file:
        json.dump(services, services_file, sort_keys=True, indent=4,)

def urlopen_logging(url, timeout=TIMEOUT):
    try:
        return opener.open(url, timeout=TIMEOUT)
    except urllib2.URLError as e:
        logging.warning("%s problem opening url %s" % (e.message, url))
        return ""
    except socket.timeout as e:
        logging.warning("%s timed out opening url %s" % (e.message, url))
        return ""

def try_open(url, ret=MAX_RETRIES, sleep=SLEEPTIME):
    page = urlopen_logging(url)
    while not page and ret:
        page = urlopen_logging(url)
        ret -= 1
        time.sleep(sleep)
    if page:
        return page
    raise urllib2.URLError("max retries reached for url %s" % url)
