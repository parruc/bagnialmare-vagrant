# -*- coding: utf-8 -*-
from lxml.html import soupparser
import utils
import json
import logging
import re

BASE_URL = "http://www.turismo.ra.it"
URL = BASE_URL + "/ita/Divertimento-e-relax/Sulla-spiaggia/Stabilimenti-balneari"
SERVICES = utils.read_services()
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)
try:
    localita = []
    bagni = []
    page = utils.try_open(URL)
    parsed_page = soupparser.parse(page)
    urls_localita = parsed_page.xpath("//div[contains(@class, 'wrapper') and contains(@class, 'intermedia')]//ul/li/a/@href")
    for url_localita in urls_localita[:-2]:
        localita_page = utils.try_open(BASE_URL + url_localita)
        parsed_localita = soupparser.parse(localita_page)
        localita = parsed_localita
        urls_bagni = parsed_localita.xpath("//div[contains(@class, 'wrapper') and contains(@class, 'intermedia')]//ul/li/a/@href")
        for url_bagno in urls_bagni:
            print "importing %s" % url_bagno
            if url_bagno in urls_localita:
                continue
            bagno = {}
            bagno_page = utils.try_open(BASE_URL + url_bagno)
            parsed_bagno = soupparser.parse(bagno_page)
            bagno['name'] = parsed_bagno.xpath("//h2[@id='contenutoPagina']/text()")[0].strip()
            available_names = {"indirizzo":"address", "telefono": "tel" , "telefax": "fax", "email": "mail", "link": "site", "sito web": "site"}
            recapito = parsed_bagno.xpath("//div[@class='sectionRight']//dl[@class='recapito']")[0]
            names = [n.strip().strip(":").lower() for n in recapito.xpath("./dt/text()")]
            contents = recapito.xpath("./dd")
            for (name, content) in zip(names, contents):
                if not name in available_names:
                    import ipdb; ipdb.set_trace()
                name = available_names[name]
                if name in ("site", "mail"):
                    bagno[name] = content.xpath(".//a/@href")[0].strip().replace("mailto:", "")
                elif name in ("tel", "fax"):
                    bagno[name] = content.text.replace("(+39) ", "").replace(".", " ").strip()
                else:
                    bagno[name] = content.text.strip()
            if "address" in bagno and "-" in bagno['address']:
                bagno['address'], bagno['city'] = bagno['address'].rsplit(" - ", 1)
            else:
                import ipdb; ipdb.set_trace
            bagno['details'] = {}
            bagno['services'] = []
            for p in parsed_bagno.xpath("//div[@class='wrapper']/p"):
                p_content = p.text_content().lower().strip()
                if u"n°" in p_content:
                    p_name, p_value = p_content.split(u"n°")
                    p_name = p_name.lower().strip()
                    p_value = int(re.sub("[^0-9]", "", p_value.lower().strip()))
                    bagno['details'][p_name] = p_value
                elif "," in p_content and not "frazione a" in p_content:
                    for service_name in  [s.strip() for s in p_content.split(",")]:
                        service_list = utils.get_service_from_alias(service_name)
                        for service in service_list:
                            service = service.strip()
                            if service:
                                if not service in SERVICES:
                                    SERVICES.append(service)
                                bagno['services'].append(service)
            bagni.append(bagno)

    utils.write_services(SERVICES)

    with open('output_ravenna.json', 'w') as outfile:
        json.dump(bagni, outfile, sort_keys=True, indent=4,)

except Exception as e:
    import ipdb; ipdb.set_trace()

