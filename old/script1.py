'''
GLN-nummer - check
kreditornummer - ?
kreditor navn - ?
fakturanummer - check
stregkode - check
varenummer - findes i tabel ud fra stregkode
linje tekst - den indeholder fsc koden - check

kreditor gln nummer findes ved at kigge efter kode UNB+UNOC. Vælg den hvor der står 3+
Den med 14+ er indeks Retails gln nummer
 Faktura nummer finde udfra kode BGM+380+  indtil +9

Faktura nummer er i dette eksempel lig 85073973

FSC kode findes også i vare beskrivelse for hver faktura linje her.

Hver fakturalinje starter med LIN+linjenummer

Efter antal og mængde kommer beskrivelse og den starter med kode IMD+F++::: beskrivelse
Det er i denne beskrivelse at i skal findes koden FSC
F.eks. som i denne fil for linie180

IMD+F++:::JUMBO BLYANT SÆT FSC 100%'

FSC koden findes ved at søge på IMD+F+M+::: også kommer fsc kode til sidst i varenavnet


stregkode findes ved kode lin+linjenummer++stregkode'''

import pandas as pd
from lxml import etree

xml_file = "../files/Burde invoice_000759106_2021-08-11-10-45-31{c732b041-f0d5-483e-b83b-3b92722a3b59}.xml"


def get_value(target_tree, xpath, namespaces):

    try:
        return target_tree.xpath(xpath, namespaces=namespaces)[0].text
    except IndexError:
        return ""


namespaces = {"cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
              "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"}

# Parse file
tree = etree.parse(xml_file)

# item descriptions and FSC
item_names = []
for item in tree.xpath("//cac:Item", namespaces=namespaces):
    item_names.append(get_value(item, "cbc:Description", namespaces))
item_names

# barcodes
barcodes = []
for code in tree.xpath("//cac:Item", namespaces=namespaces):
    barcodes.append(get_value(code, "cbc:ID", namespaces))
barcodes


# GLN
customer = tree.xpath("//cac:AccountingCustomerParty", namespaces=namespaces)
c = customer.pop()
gln = get_value(c, "//cbc:EndpointID", namespaces)
gln = get_value(c, "//cac:PartyIdentification", namespaces)


# invoice number



"""

df = pd.read_xml(xml_file,
                 xpath="//InvoiceLine")

import xml.etree.ElementTree as ET
mytree = ET.parse(xml_file)
myroot = mytree.getroot()
for x in myroot[0]:
     print(x.tag, x.attrib)

for x in myroot.findall('AccountingSupplierParty'):
    item = x.find('Party').text

from xml.dom import minidom
dat=minidom.parse(xml_file)

tagname= dat.getElementsByTagName('cac:PaymentMeans')
print(tagname.firstChild.data)

for x in tagname:
    print(x.firstChild.data)"""

root.find("{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoiceLine").text

root = root.findall("{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingCustomerParty")

for i in elements:
    print(i)


root = ET.fromstring(xml_string)

for child in root:
    print(child.tag,"  :::  ", child.attrib)

