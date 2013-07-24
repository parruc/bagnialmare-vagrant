# -*- coding: utf-8 -*-
import utils
import simplejson
import logging
import re

BASE_URL = "http://www.turismo.comunecervia.it"
URL = BASE_URL + "/divertimento_relax/sulla_spiaggia/stabilimenti_balneari/"
SERVICES = utils.read_services()
DETAILS = utils.read_details()
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
bagni = []
name_from_title = re.compile("([0-9\-/]+) (.+)")
numbers_from_text = re.compile("([^0-9^-^(^)]+)([0-9][0-9,.-]*)")
arernile_demaniale = re.compile(" - Arenile demaniale [0-9]+")
parsed_page = utils.try_open_file_or_url(url=URL, name="cervia", count=1)
trs = parsed_page.xpath("//table/tbody/tr")
columns = ["name", "address", "city", "tel", "fax", "mail", "site"]

for i, tr in enumerate(trs, start=1):
    parsed_bagno = None
    bagno = {}
    tds = tr.xpath("./td")
    for column, td in zip(columns, tds):
        td_content = td.text_content().strip()
        if not td_content:
            continue
        if column == "name":
            match = name_from_title.match(td_content)
            if not match:
                import ipdb; ipdb.set_trace()
            bagno['number'] = match.group(1).strip()
            bagno['name'] = match.group(2).strip()

            bagno_url = td.xpath("./a/@href")[0].replace("../../../..", BASE_URL)
            parsed_bagno = utils.try_open_file_or_url(url=bagno_url, name="cervia_bagno", count=i)
        elif column in ["mail", "site"]:
            href = td.xpath("./a/@href")
            if len(href):
                bagno[column] = href[0].replace("mailto:", "")
        elif column == "tel":
            for tel in td_content.split("-"):
                tel = tel.strip()
                if tel.startswith("05"):
                    field = "tel"
                elif tel.startswith("3"):
                    field = "cell"
                else:
                    field = "tel"
                    tel = "0544 " + tel
                if field in bagno:
                    bagno[field] += " - " + tel
                else:
                    bagno[field] = tel
        else:
            bagno[column] = td_content
    if "address" in bagno:
        bagno['address'] = arernile_demaniale.sub("", bagno['address'])
    logging.info("Parsing cervia number %d name %s" % (i, bagno['name']))
    if parsed_bagno is None:
        import ipdb; ipdb.set_trace()
    fields = parsed_bagno.xpath("//*[@class='bold blu']")
    bagno['services'] = []
    bagno['details'] = {}
    for field in fields:
        field_name = field.text.replace(":", "").strip().lower()
        field_values = field.xpath("./following-sibling::text()")
        if len(field_values) and len("".join(field_values).strip()) > 0:
            field_values = " ".join(field_values).strip()
        else:
            field_values = field.xpath("./following-sibling::*[not(@class='bold blu')]")
            if len(field_values) > 0:
                field_values = field_values[0].text_content()
            else:
                field_values = ""

        if field_name == "servizi offerti":
            for field_value in field_values.split("-"):
                matches = numbers_from_text.findall(field_value)
                if matches:
                    for match in matches:
                        try:
                            detail_name = utils.get_detail_from_alias(match[0].strip().strip("numero").strip("n.").strip("mq").strip("m").strip("n").strip().strip(":").strip(".").strip().lower())
                            if detail_name.startswith("service:"):
                                service_list = utils.get_service_from_alias(detail_name.replace("service:", ""))
                                for service in service_list:
                                    if service:
                                        if not service in SERVICES:
                                            SERVICES.append(service)
                                        if not service in bagno['services']:
                                            bagno['services'].append(service)
                            else:
                                detail_value = int(float(match[1].replace(".", "").replace(",", ".").strip()))
                                if detail_name:
                                    if not detail_name in DETAILS:
                                        DETAILS.append(detail_name)
                                    if not detail_name in bagno['details']:
                                        bagno['details'][detail_name] = detail_value
                        except Exception:
                            import ipdb; ipdb.set_trace()
                            pass
                else:
                    service_list = field_value.strip().lower()
                    service_list = re.sub(u' n?°?\.? ?[0-9]?$', '', service_list)
                    service_list = re.sub(u'[0-9]', '', service_list)
                    service_list = service_list.strip()
                    service_list = utils.get_service_from_alias(service_list)
                    for service in service_list:
                        if service:
                            if not service in SERVICES:
                                SERVICES.append(service)
                            if not service in bagno['services']:
                                bagno['services'].append(service)

        elif field_name == u"attività":
            field_value = field_values.replace(":", "").strip().strip(".").lower()
            for field_value in re.split("\n|-|\.", field_value):
                service_list = field_value.strip().lower()
                service_list = re.sub(u' n?°?\.? ?[0-9]?$', '', service_list)
                service_list = re.sub(u'[0-9]', '', service_list)
                service_list = service_list.strip()
                service_list = utils.get_service_from_alias(service_list)
                for service in service_list:
                    if service:
                        if service.startswith("giochi per bambini"):
                            service = "baby park"
                        if not service in SERVICES:
                            SERVICES.append(service)
                        if not service in bagno['services']:
                            bagno['services'].append(service)

        elif not field_name in ['associazione di riferimento', 'tariffe', 'come arrivare', 'periodo di apertura']:
            field_value = field_values.replace(":", "").strip().lower()
            matches = numbers_from_text.findall(field_name + field_value)
            if matches:
                for match in matches:
                    try:
                        detail_name = utils.get_detail_from_alias(match[0].strip().strip("numero").strip("n.").strip("mq").strip("m").strip("n").strip().strip(":").strip(".").strip().lower())
                        if detail_name.startswith("service:"):
                                service_list = utils.get_service_from_alias(detail_name.replace("service:", ""))
                                for service in service_list:
                                    if service:
                                        if not service in SERVICES:
                                            SERVICES.append(service)
                                        if not service in bagno['services']:
                                            bagno['services'].append(service)
                        else:
                            detail_value = int(float(match[1].replace(".", "").replace(",", ".").strip()))
                            if detail_name:
                                if not detail_name in DETAILS:
                                    DETAILS.append(detail_name)
                                if not detail_name in bagno['details']:
                                    bagno['details'][detail_name] = detail_value
                    except Exception:
                        import ipdb; ipdb.set_trace()
                        pass
            else:
                if not field_name in ['associazione di riferimento', 'tariffe', 'come arrivare', 'periodo di apertura']:
                    service_names = field_name + field_value
                    if service_names.startswith("giochi per bambini"):
                        service_names = "baby park"
                    elif service_names.startswith("ristorazionepiccola"):
                        service_names = "piccola ristorazione"
                    elif service_names.startswith("animazionemini"):
                        if "feste a tema" in service_names:
                            service_names = "feste a tema\nanimazione per bambini"
                        else:
                            service_names = "animazione per bambini"
                    elif service_names.startswith("dotazioni sportive"):
                        service_names = field_value.replace(",", "\n")
                    for service_name in re.split("\n|\.", service_names.strip(".")):
                        service_list = service_name.strip().lower()
                        service_list = re.sub(u' n?°?\.? ?[0-9]?$', '', service_list)
                        service_list = re.sub(u'[0-9]', '', service_list)
                        service_list = service_list.strip()
                        service_list = utils.get_service_from_alias(service_list)
                        for service in service_list:
                            if service:
                                if not service in SERVICES:
                                    SERVICES.append(service)
                                if not service in bagno['services']:
                                    bagno['services'].append(service)
    bagni.append(bagno)

utils.write_services(SERVICES)
utils.write_details(DETAILS)

with open('output_cervia.json', 'w') as outfile:
  simplejson.dump(bagni, outfile, sort_keys=True, indent=4,)
