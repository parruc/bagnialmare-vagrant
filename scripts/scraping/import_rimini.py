# -*- coding: utf-8 -*-
import utils
import simplejson
import logging
import re

BASE_URL = "http://www.riminiturismo.it"
URL = BASE_URL + "/uWeb/main.php?rimtur3=jms5q77caab1en9vf9g5bovca4&lang_index=0&elemId=124&elemId=124&search=1&layout=print"
SERVICES = utils.read_services()
DETAILS = utils.read_details()
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
bagni = []
name_and_number_from_title = re.compile("((Bagno ([0-9\-/A-D]*) (sud|nord)?[ -]*(.+)?)|(.+))")
replace_number_insensitive = re.compile("per clienti", re.IGNORECASE)
# arernile_demaniale = re.compile(" - Arenile demaniale [0-9]+")
parsed_page = utils.try_open_file_or_url(url=URL, name="rimini", count=1)
trs = parsed_page.xpath("//table/tbody/tr")


for i, tr in enumerate(trs, start=1):
    parsed_bagno = None
    bagno = {}
    td = tr.xpath(".//td")[0]
    bagno_name = td.text_content().strip()
    match = name_and_number_from_title.match(bagno_name)
    if match:
        if match.group(3) and match.group(5):
            bagno['number'] = match.group(3)
            bagno['name'] = match.group(5)
        else:
            bagno['name'] = match.group(0)
    else:
        import ipdb; ipdb.set_trace()
    logging.info("Parsing %s" % bagno['name'])
    bagno_url = td.xpath("./a/@href")[0]
    parsed_bagno = utils.try_open_file_or_url(url=bagno_url, name="rimini_bagno", count=i)
    if parsed_bagno is None:
        import ipdb; ipdb.set_trace()

    bagno_address = parsed_bagno.xpath("//div[@id='sviluppo']//p[@class='sottotitolo_content']")
    if bagno_address:
        bagno['address'] = bagno_address[0].text_content().strip()
    sviluppo = parsed_bagno.xpath("//div[@id='sviluppo']")[0]
    bagno_details = sviluppo.xpath("./div[@class='linea1']|./div[@class='linea2']")
    bagno['services'] = []
    bagno['details'] = {}
    for bagno_detail in bagno_details:
        titoletto = bagno_detail.xpath("./span[@class='titoletto']")
        if len(titoletto) > 0 and titoletto[0].text_content().strip() != "":
            titoletto = titoletto[0]
            titoletto_text = titoletto.text_content().strip()
            detail_text = bagno_detail.text_content().replace(titoletto_text, "", 1).replace(":", "").strip("\r\n\t -").lower()
            if titoletto_text == u"Telefono":
                for detail_text in re.split("[\-,]", detail_text):
                    detail_text = detail_text.replace("+39", "").strip().replace("cell.", "")
                    if detail_text.startswith("05"):
                        field = "tel"
                    else:
                        field = "cell"
                    if field in bagno:
                        bagno[field] += " - " + detail_text
                    else:
                        bagno[field] = detail_text
            elif titoletto_text == u"Recapito periodo invernale":
                if 'winter_tel' in bagno:
                    bagno['winter_tel'] += " " + detail_text
                else:
                    bagno['winter_tel'] = detail_text
            elif titoletto_text == u"Indirizzo":
                bagno['address'] = detail_text
            elif titoletto_text == u"Fax":
                bagno['fax'] = detail_text.replace("informazioni e prenotazioni", "per info")
            elif titoletto_text == u"Località":
                bagno['city'] = detail_text
            elif titoletto_text == u"Email":
                bagno['mail'] = detail_text
            elif titoletto_text == u"www":
                bagno['site'] = bagno_detail.xpath("./a/@href")[0]
            elif titoletto_text == u"Numero Ombrelloni":
                detail_num = replace_number_insensitive.sub("", detail_text.split("/")[0]).strip("\t\n\r -")
                bagno['details']['ombrelloni'] = int(detail_num)
            elif titoletto_text == u"Numero Cabine":
                detail_num = replace_number_insensitive.sub("", detail_text.split("/")[0]).strip("\t\n\r -")
                bagno['details']['cabine'] = int(detail_num)
            elif titoletto_text == u"Servizi offerti":
                if 'description' in bagno:
                    bagno['description'] += " " + titoletto_text + " " + detail_text
                else:
                    bagno['description'] = titoletto_text + " " + detail_text
            elif titoletto_text == u"Ristorazione":
                if "ristorazione" not in bagno['services']:
                    bagno['services'].append("Ristorazionezione")
            elif titoletto_text in ["Orario feriale", "Orario festivo", "Data ultimo aggiornamento", "Come arrivare", "Periodo di apertura", "Chiusura settimanale"]:
                pass
            else:
                if 'description' in bagno:
                    bagno['description'] += " " + titoletto_text + " " + detail_text
                else:
                    bagno['description'] = titoletto_text + " " + detail_text
        else:
            service_name = bagno_detail.text_content().strip("\n\r\t -")
            if service_name.lower() in ["non accettano carte di credito", "non si accettano carte di credito"]:
                pass
            elif service_name in ("Acceso ai cani", ):
                service_list = utils.get_service_from_alias(service_name.lower())
                for service in service_list:
                    if service:
                        if not service in SERVICES:
                            SERVICES.append(service)
                        if not service in bagno['services']:
                            bagno['services'].append(service)
            else:
                if 'description' in bagno:
                    bagno['description'] += " " + service_name
                else:
                    bagno['description'] = service_name
    bagno_services = sviluppo.xpath("./fieldset/div[@class='linea1']|/div[@class='linea2']")
    for bagno_service in bagno_services:
        service_list = utils.get_service_from_alias(bagno_service.text_content().strip().lower())
        for service in service_list:
            if service:
                if not service in SERVICES:
                    SERVICES.append(service)
                if not service in bagno['services']:
                    bagno['services'].append(service)
    if not "city" in bagno:
        bagno["city"] = "Rimini"
    bagni.append(bagno)


utils.write_services(SERVICES)
utils.write_details(DETAILS)

with open('output_rimini.json', 'w') as outfile:
    simplejson.dump(bagni, outfile, sort_keys=True, indent=4,)
