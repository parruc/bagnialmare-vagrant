# -*- coding: utf-8 -*-
import utils
import simplejson
import logging
import re

BASE_URL = "http://www.turismo.comunecervia.it"
URL = BASE_URL + "/divertimento_relax/sulla_spiaggia/stabilimenti_balneari/"
SERVICES = utils.read_services()
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)
bagni = []
name_from_title = re.compile("([0-9\-/]+) (.+)")

parsed_page = utils.try_open_file_or_url(url=URL, name="cervia", count=1)
trs = parsed_page.xpath("//table/tbody/tr")
columns = ["name", "address", "city", "tel", "fax", "mail", "site"]
for i, tr in enumerate(trs, start=1):
    parsed_bagno = None
    bagno = {}
    tds = tr.xpath("./td")
    for column, td in zip(columns, tds):
        td_content = td.text_content().strip()
        if column == "name":
            match = name_from_title.match(td_content)
            if not match:
                import ipdb; ipdb.set_trace()
            bagno['number'] = match.group(1).strip()
            bagno['name'] = match.group(2).strip()
            bagno_url = td.xpath("./a/@href")[0].replace("../../../..", BASE_URL)
            parsed_bagno = utils.try_open_file_or_url(url=bagno_url, name="cervia", count=i)
        elif column in ["mail", "site"]:
            bagno_url = td.xpath("./a/@href")
            if len(bagno_url):
                bagno[column] = bagno_url[0].replace("mailto:", "")
        else:
            bagno[column] = td_content
    if not parsed_bagno:
        import ipdb; ipdb.set_trace()
    fields = [u"servizi offerti", u"ristorazione", u"attività"]
    import ipdb; ipdb.set_trace()
    for field_name in fields:
        field_value = parsed_bagno.xpath("//div[@class='div_testo']//*[@class='bold blu][text()='" + field_name + "']/following-sibling::text()")

