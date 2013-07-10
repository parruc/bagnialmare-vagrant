# -*- coding: utf-8 -*-
from lxml.html import soupparser
import urllib2
import os
import socket
import logging
import time
import types
import simplejson

TIMEOUT = 5
MAX_RETRIES = 3
SLEEPTIME = 5

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")]

def read_service_aliases():
    try:
        with open('services_aliases.json', 'r') as aliases_file:
            return simplejson.load(aliases_file)
    except IOError:
        return []

def get_service_from_alias(service_name):
    service_list = [service_name, ]
    ALIASES = read_service_aliases()
    if service_name in ALIASES:
        service_list = ALIASES[service_name]
        if isinstance(service_list, types.StringTypes):
            service_list = [service_list, ]
    return service_list

def read_services():
    try:
        with open('services.json', 'r') as services_file:
            return simplejson.load(services_file)
    except IOError:
        return []

def write_services(services):
    with open('services.json', 'w') as services_file:
        simplejson.dump(services, services_file, sort_keys=True, indent=4,)

def read_details():
    try:
        with open('details.json', 'r') as services_file:
            return simplejson.load(services_file)
    except IOError:
        return []

def read_details_aliases():
    try:
        with open('details_aliases.json', 'r') as aliases_file:
            return simplejson.load(aliases_file)
    except IOError:
        return []

def get_detail_from_alias(detail_name):
    ALIASES = read_details_aliases()
    if detail_name in ALIASES:
        return ALIASES[detail_name]
    return detail_name

def write_details(services):
    with open('details.json', 'w') as services_file:
        simplejson.dump(services, services_file, sort_keys=True, indent=4,)

def urlopen_logging(url, timeout=TIMEOUT):
    try:
        return opener.open(url, timeout=TIMEOUT)
    except urllib2.URLError as e:
        logging.warning("%s problem opening url %s" % (e.message, url))
        return ""
    except socket.timeout as e:
        logging.warning("%s timed out opening url %s" % (e.message, url))
        return ""

def try_open_file_or_url(url, name=None, count=None, ret=MAX_RETRIES, sleep=SLEEPTIME):
    if name and count:
        file_name = "html_dump/%s_%d.html" % (name, count)
        if os.path.exists(file_name):
            with open(file_name, 'r') as html_file:
                return soupparser.parse(html_file)
        return try_open_url(url=url, file_name=file_name, ret=ret, sleep=sleep)
    return try_open_url(url=url, ret=ret, sleep=sleep)


def try_open_url(url, file_name=None, ret=MAX_RETRIES, sleep=SLEEPTIME):
    page = urlopen_logging(url)
    while not page and ret:
        page = urlopen_logging(url)
        ret -= 1
        time.sleep(sleep)
    if page:
        html_string = page.read()
        if file_name:
            with open(file_name, 'w') as html_file:
                html_file.write(html_string)
        return soupparser.fromstring(html_string)
    raise urllib2.URLError("max retries reached for url %s" % url)

