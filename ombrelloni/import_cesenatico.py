from lxml.html import soupparser
import urllib2
import socket
import json
import logging
import re
import time

BASE_URL = "http://web.comune.cesenatico.fc.it/turismo/"
URL = BASE_URL + "elenco_schede.asp?ambiente=DIVERTIMENTO%20E%20RELAX&famiglia=SULLA%20SPIAGGIA&sottofamiglia=STABILIMENTI%20BALNEARI&p="
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")]
TIMEOUT = 5
MAX_RETRIES = 3
SLEEPTIME = 5
SERVICES = []
with open('services.json', 'r') as services_file:
    SERVICES = json.load(services_file)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)
tel_from_text = re.compile("Tel: ([0-9 ]+)")
fax_from_text = re.compile("Fax: ([0-9 ]+)")
mail_from_text = re.compile("[a-zA-z]{1}[\w.-]+@[\w.-]+")
site_from_text = re.compile("(?:http://www\.|http://|www\.)[\w.\-]+\.[\w]{,3}")
city_from_text = re.compile("[0-9]+ (\w+)[ ]+- (\w+) \(FC\)")
geo_from_text = re.compile("LatLng\(([0-9.]+),([0-9.]+)\);")
number_from_detail = re.compile("[^0-9]*([0-9]+[.,]{,1}[0-9]{,1})[^0-9]*")


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

url_bagni = []
for page_number in range(1,14):
    page = try_open(URL + str(page_number))
    parsed_page = soupparser.parse(page)
    url_bagni_new = [BASE_URL + p.replace(" ", "%20") for p in parsed_page.xpath("//div[@class='categories-sublist']/ul/li/a/@href") if not p == "http://"]
    url_bagni += url_bagni_new
    logging.info("Added %d elements to parse list for page %d" % (len(url_bagni_new), page_number, ))

bagni = []
for url_bagno in url_bagni:
    logging.info("Startes parsing %s to parse list" % url_bagno)
    bagno = {}
    bagno_page = try_open(url_bagno)
    parsed_bagno = soupparser.parse(bagno_page)
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
        bagno['tel'] = tel[0]
    else:
        missing.append("tel")
    if len(fax):
        bagno['fax'] = fax[0]
    else:
        missing.append("fax")
    if len(mail):
        bagno['mail'] = mail[0]
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
                        import ipdb; ipdb.set_trace()
                    detail_value = "0"
                else:
                    detail_value = match.group(1).replace(".", "").strip(",").replace(",", ".").strip()
                try:
                    bagno['details'][detail_name] = int(float(detail_value))
                except:
                    import ipdb; ipdb.set_trace()
        else:
            for single_service in bagno_details_row.strip(".").strip(",").split(","):
                service = single_service.replace(";", "").replace(".", "").lower().strip()
                if service:
                    if not service in SERVICES:
                        SERVICES.append(service)
                    bagno['services'].append(service)

    parsed_bagno.xpath("//script/text()")
    bagno['coords'] = geo_from_text.findall(" ".join(parsed_bagno.xpath("//script/text()")))
    bagni.append(bagno)

with open('services.json', 'w') as services_file:
    json.dump(SERVICES, services_file, sort_keys=True, indent=4,)

with open('output_cesenatico.json', 'w') as outfile:
  json.dump(bagni, outfile, sort_keys=True, indent=4,)
