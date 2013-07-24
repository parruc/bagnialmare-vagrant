# -*- coding: utf-8 -*-
import utils
import simplejson
import logging
import re


URL="http://www.ferraraterraeacqua.it/it/divertimento-e-relax/sulla-spiaggia/stabilimenti-balneari/@@bath_results?name=&submit=Cerca&localita_id="
SERVICES = utils.read_services()
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)
coords_from_url = re.compile(".*/maps\?q=([0-9.]+), ([0-9.]+)")
name_from_title = re.compile("(.+?)\.? (.+)")

bagni = []
parsed_page = utils.try_open_file_or_url(url=URL, name="ferrara", count=1)
url_bagni = parsed_page.xpath("//div[@class='results']/ul/li/a/@href")
for i, url_bagno in enumerate(url_bagni, start=1):
    bagno = {}
    parsed_bagno = utils.try_open_file_or_url(url=url_bagno, name="ferrara_bagno", count=i)
    bagno_title = parsed_bagno.xpath("//h2[@class='detail-name']")[0].text.strip()
    match = name_from_title.match(bagno_title)
    if not match:
        import ipdb; ipdb.set_trace()
    bagno['number'] = match.group(1)
    bagno['name'] = match.group(2)
    logging.info("Parsing %s" % bagno['name'])
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
        for tel in re.split("(-|cell\.)", bagno_details[2].text.strip()):
            tel = tel.strip()
            if tel in ["-", ""]:
                continue
            if tel.startswith("05"):
                name = "tel"
            else:
                name = 'cell'
            if name in bagno:
                bagno[name] += " - " + tel
            else:
                bagno[name] = tel
    if len(bagno_details) > 3:
        bagno['mail'] = bagno_details[3].text_content().strip()
    if len(bagno_details) > 4:
        bagno['site'] = bagno_details[4].text_content().strip()
    if len(bagno_details) > 5:
        import ipdb; ipdb.set_trace()
    bagno['services'] = []
    service_tds = parsed_bagno.xpath("//fieldset[@class='detail-facilities']//td")
    for service_td in service_tds:
        service_name = service_td.text.strip().lower()
        service_list = utils.get_service_from_alias(service_name)
        for service in service_list:
            if service:
                if not service in SERVICES:
                    SERVICES.append(service)
                if not service in bagno['services']:
                    bagno['services'].append(service)
    bagno_geolink = parsed_bagno.xpath("//p[@class='geoRefLink']//a/@href")
    match = coords_from_url.match(bagno_geolink[0])
    if not match:
        import ipdb; ipdb.set_trace()
    bagno['coords'] = (match.group(1), match.group(2),)
    bagni.append(bagno)

utils.write_services(SERVICES)

with open('output_ferrara.json', 'w') as outfile:
  simplejson.dump(bagni, outfile, sort_keys=True, indent=4,)
