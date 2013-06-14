from lxml.html import soupparser
import urllib2
import socket
import json
import logging
import re
import time

URL="http://www.ferraraterraeacqua.it/it/divertimento-e-relax/sulla-spiaggia/stabilimenti-balneari/@@bath_results?name=&submit=Cerca&localita_id="
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")]
TIMEOUT = 5
MAX_RETRIES = 3
SERVICES = []
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)
coords_from_url = re.compile(".*/maps\?q=([0-9.]+), ([0-9.]+)")
name_from_title = re.compile("(.+)\.? (.+)")

def urlopen_logging(url, timeout=TIMEOUT):
    try:
        return opener.open(url, timeout=TIMEOUT)
    except urllib2.URLError as e:
        logging.warning("Warning %s opening url %s" % (e.message, url))
        return ""
    except socket.timeout as e:
        logging.warning("Warning %s opening url %s" % (e.message, url))
        return ""
bagni = []
page = urlopen_logging(URL)
ret = MAX_RETRIES
while not page and ret:
        time.sleep(6)
        page = urlopen_logging(URL)
        ret -= 1
parsed_page = soupparser.parse(page)
url_bagni = parsed_page.xpath("//div[@class='results']/ul/li/a/@href")
for url_bagno in url_bagni:
    bagno = {}
    bagno_page = urlopen_logging(url_bagno)
    ret = MAX_RETRIES
    while not bagno_page and ret:
        time.sleep(6)
        bagno_page = urlopen_logging(url_bagno)
        ret -=1
    parsed_bagno = soupparser.parse(bagno_page)
    bagno_title = parsed_bagno.xpath("//h2[@class='detail-name']")[0].text.strip()
    match = name_from_title.match(bagno_title)
    if not match:
        import ipdb; ipdb.set_trace()
    bagno['number'] = match.group(1)
    bagno['name'] = match.group(2)
    for bad in parsed_bagno.xpath("//div[@class='detail-contact']/div[strong[text()='fax']]"):
        bad.drop_tree()
    for bad in parsed_bagno.xpath("//div[@class='detail-contact']/div//strong"):
        bad.drop_tree()
    bagno_details = parsed_bagno.xpath("//div[@class='detail-contact']/div")
    if len(bagno_details) > 0:
        bagno['address'] = bagno_details[0].text.strip()
    if len(bagno_details) > 1:
        bagno['city'] = bagno_details[1].text.strip()
    if len(bagno_details) > 2:
        bagno['tel'] = bagno_details[2].text.strip()
    if len(bagno_details) > 3:
        bagno['mail'] = bagno_details[3].text_content().strip()
    if len(bagno_details) > 4:
        bagno['site'] = bagno_details[4].text_content().strip()
    if len(bagno_details) > 5:
        import ipdb; ipdb.set_trace()
    bagno_services = []
    service_tds = parsed_bagno.xpath("//fieldset[@class='detail-facilities']//td")
    for service_td in service_tds:
        service_name = service_td.text.strip().lower()
        if service_name:
            if not service_name in SERVICES:
                SERVICES.append(service_name)
            bagno_services.append(service_name)
    bagno['services'] = bagno_services
    bagno_geolink = parsed_bagno.xpath("//p[@class='geoRefLink']//a/@href")
    match = coords_from_url.match(bagno_geolink[0])
    if not match:
        import ipdb; ipdb.set_trace()
    bagno['coords'] = (match.group(1), match.group(2),)
    bagni.append(bagno)

with open('output_ferrara.json', 'w') as outfile:
  json.dump(bagni, outfile, sort_keys=True, indent=4,)
