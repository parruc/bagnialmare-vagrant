# -*- coding: utf-8 -*-
import simplejson
import logging
import re
import utils

BASE_URL = "http://web.comune.cesenatico.fc.it/turismo/"
URL = BASE_URL + "elenco_schede.asp?ambiente=DIVERTIMENTO%20E%20RELAX&famiglia=SULLA%20SPIAGGIA&sottofamiglia=STABILIMENTI%20BALNEARI&p="
SERVICES = utils.read_services()
DETAILS = utils.read_details()
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)
tel_from_text = re.compile("Tel: ([0-9 \.]+)")
fax_from_text = re.compile("Fax: ([0-9 \.]+)")
mail_from_text = re.compile("[a-zA-z]{1}[\w.-]+@[\w.-]+")
site_from_text = re.compile("(?:http://www\.|http://|www\.)[\w.\-]+\.[\w]{,3}")
city_from_text = re.compile("[0-9]+ (\w+)[ ]+- (\w+) \(FC\)")
geo_from_text = re.compile("LatLng\(([0-9.]+) *, *([0-9.]+)\);")
number_from_detail = re.compile("[^0-9]*([0-9]+[0-9.,]*)[^0-9]*")
clean_email = re.compile("(http|www).*")


url_bagni = []
for page_number in range(1,14):
    parsed_page = utils.try_open_file_or_url(url=URL + str(page_number), name="cesenatico_paging", count=page_number)
    url_bagni_new = [BASE_URL + p.replace(" ", "%20") for p in parsed_page.xpath("//div[@class='categories-sublist']/ul/li/a/@href") if not p == "http://"]
    url_bagni += url_bagni_new
    logging.info("Added %d elements to parse list for page %d" % (len(url_bagni_new), page_number, ))

bagni = []
for i, url_bagno in enumerate(url_bagni, start=1):
    logging.info("Startes parsing %s to parse list" % url_bagno)
    bagno = {}
    parsed_bagno = utils.try_open_file_or_url(url=url_bagno, name="cesenatico_bagno", count=i)
    bagno['name'] = parsed_bagno.xpath("//h2[@class='titolo-scheda']")[0].text.strip().capitalize()
    bagno_contacts = parsed_bagno.xpath("//div[@class='block-address']//div[@class='frame']/p/span")
    bagno['address'] = bagno_contacts[0].text.strip()

    match = city_from_text.match(bagno_contacts[1].text.strip())
    if not match:
        import ipdb; ipdb.set_trace()
    bagno['city'] = match.group(1) + " " + match.group(2)

    contacts = bagno_contacts[2].text_content().strip()
    tel = tel_from_text.findall(contacts)
    fax = fax_from_text.findall(contacts)
    mail = mail_from_text.findall(contacts)
    site = site_from_text.findall(contacts)
    missing = []
    if len(tel):
        if tel[0].startswith("05"):
            field = "tel"
        else:
            field = "cell"
        bagno[field] = tel[0]
    else:
        missing.append("tel")
    if len(fax):
        bagno['fax'] = fax[0]
    else:
        missing.append("fax")
    if len(mail):
        mail = clean_email.sub("", mail[0])
        bagno['mail'] = mail
    else:
        missing.append("mail")
    if len(site):
        bagno['site'] = site[0]
    else:
        missing.append("SITE")
    if len(missing):
        logging.warning("%s does not contains %s" % (contacts, " ".join(missing)))

    bagno_details_rows = parsed_bagno.xpath("//div[@id='content']/p/strong[text()='Servizi offerti:']/following-sibling::text()")
    bagno['details'] = {}
    bagno['services'] = []
    for bagno_details_row in bagno_details_rows:
        if ":" in bagno_details_row:
            for bagno_detail in bagno_details_row.split(";"):
                if len(bagno_detail.split(":")) < 2:
                    continue
                detail_name, detail_value = bagno_detail.split(":")
                detail_name = detail_name.strip().lower()
                if len(detail_name) == 0:
                    continue
                match = number_from_detail.match(detail_value)
                if not match:
                    if not "-" in detail_value:
                        if "Sala tv" in detail_value:
                            bagno['services'].append("sala tv")
                            continue
                    detail_value = "0"
                else:
                    detail_value = match.group(1).replace(".", "").strip(",").replace(",", ".").strip()
                try:
                    detail_name = utils.get_detail_from_alias(detail_name)
                    if detail_name:
                        if detail_name.startswith("service:"):
                            service_list = utils.get_service_from_alias(detail_name.replace("service:", ""))
                            for service in service_list:
                                if service:
                                    if not service in SERVICES:
                                        SERVICES.append(service)
                                    if not service in bagno['services']:
                                        bagno['services'].append(service)
                        else:
                            if not detail_name in DETAILS:
                                DETAILS.append(detail_name)
                            if not detail_name in bagno['details']:
                                bagno['details'][detail_name] = int(float(detail_value))
                except Exception:
                    import ipdb; ipdb.set_trace()
        else:
            for single_service in bagno_details_row.strip(".").strip(",").split(","):
                service_name = single_service.replace(";", "").replace(".", "").lower().strip()
                service_list = utils.get_service_from_alias(service_name)
                for service in service_list:
                    if service:
                        if not service in SERVICES:
                            SERVICES.append(service)
                        if not service in bagno['services']:
                            bagno['services'].append(service)

    parsed_bagno.xpath("//script/text()")
    coords = geo_from_text.findall(" ".join(parsed_bagno.xpath("//script/text()")))
    if len(coords):
        bagno['coords'] = coords[0]
    else:
        import ipdb; ipdb.set_trace()
    bagni.append(bagno)

utils.write_services(SERVICES)
utils.write_details(DETAILS)

with open('output_cesenatico.json', 'w') as outfile:
  simplejson.dump(bagni, outfile, sort_keys=True, indent=4,)
