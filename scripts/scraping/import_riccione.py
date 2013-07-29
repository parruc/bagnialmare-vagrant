# -*- coding: utf-8 -*-
from lxml import html
import utils
import simplejson
import logging
import re


URL="http://www.riccione.it/spiaggia/default.asp?id=1395"
#SERVICES = utils.read_services()
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)

bagni = []
parsed_page = utils.try_open_file_or_url(url=URL, name="riccione", count=1)
trs = parsed_page.xpath("//table[@class='colore_filetto_tabelle']//table//table//tr")
for i, tr in enumerate(trs[1:], start=1):
    bagno = {}
    # Usless coords found in http://www.riccione.it/mappa/xml/spiaggia_5.xml used by http://www.riccione.it/default.asp?id=9305&id2=2263&id3=33
    tds = tr.xpath("./td")
    for txt in [t.strip() for t in tds[0].xpath(".//text()") if t.strip()]:
        if txt and not txt[0].isdigit():
            bagno['name'] = txt
    numbers = tds[0].xpath(".//span")
    if len(numbers) > 0:
        bagno['number'] = "/".join([n.text_content().strip() for n in numbers])
        for n in numbers:
            n.drop_tag()
    if bagno['name'] in ("Spiaggia", "La Spiaggia"):
        bagno['name'] += u" " + bagno['number']
    if bagno['name'] in ("Spiaggia libera", "Colonie"):
        continue
    print "Parsing %s" % bagno['name']
    telephones = re.split('[\n\r\t\-]', html.fromstring(html.tostring(tds[1]).replace("<br>", "\n")).text_content())
    for telephone in telephones:
        telephone = telephone.strip().strip(".").strip().lower()
        if telephone:
            num = telephone.split(" ")[-1]
            for field, name in {"tel": "tel", "fax": "fax", "cell": "cell", "winter_tel": "recapito invernale"}.items():
                if name in telephone:
                    if field in bagno:
                        bagno[field] += " - " + num
                    else:
                        bagno[field] = num
    bagno_mail = tds[2].xpath("./a/@href")
    if bagno_mail:
        bagno['mail'] = bagno_mail[0].replace("mailto:", "").strip()

    bagno_site = tds[3].xpath("./a/@href")
    if bagno_site:
        bagno['site'] = bagno_site[0].strip()

    bagno_address = tds[4].text_content().strip()
    if bagno_address:
        if bagno_address == "Centro":
            bagno_address = "Riccione centro"
        bagno['address'] = bagno_address
    bagno['city'] = "Riccione"

    bagni.append(bagno)

with open('output_riccione.json', 'w') as outfile:
  simplejson.dump(bagni, outfile, sort_keys=True, indent=4,)
