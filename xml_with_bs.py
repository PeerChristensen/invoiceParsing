from bs4 import BeautifulSoup as bs4
import pandas as pd


def get_xml_content(file: str) -> bs4:
    """
    Read content from an xml file.
    Returns a 'BeautifulSoup object'
    """
    content = open(file, "r", encoding="utf8").read()
    soup = bs4(content, "xml")
    return soup


def get_creditor_gln_xml(soup: bs4) -> int:
    """Get Creditor GLN from xml file"""
    acp_tag = soup.find("cac:AccountingCustomerParty")
    creditor_gln = acp_tag.PartyIdentification.ID.text
    return creditor_gln


def get_invoice_no_xml(soup: bs4) -> str:
    """Get invoice number from xml file"""
    invoice_no = soup.find("cbc:ID").text
    return invoice_no


def get_items_xml(soup: bs4) -> bs4:
    """Get all 'Item' tags from xml"""
    items = soup.findAll("cac:Item")
    return items


def get_barcodes_xml(items: bs4) -> list:
    """Get list of barcodes from xml file"""
    barcodes = []
    for i in items:
        try:
            barcodes.append(i.ID.text)
        except:
            barcodes.append("")
    return barcodes


def get_name_and_fsc_xml(items: bs4) -> list:
    """Get product name/description and FSC info"""
    items_descriptions = []
    for i in items:
        try:
            items_descriptions.append(i.Description.text)
        except:
            items_descriptions.append("")
    return items_descriptions


def make_df_from_xml_file(file: str) -> pd.DataFrame:
    """
    This function calls various helper functions to create a dataframe after parsing
    the relevant content from .xml files.
    """
    content = get_xml_content(file)                # get content
    cred_gln_no = get_creditor_gln_xml(content)    # get creditor GLN number
    inv_no = get_invoice_no_xml(content)           # get invoice number
    items = get_items_xml(content)                         # get items
    barcodes = get_barcodes_xml(items)           # get barcodes
    names_and_fsc = get_name_and_fsc_xml(items)  # get names and FSC codes

    df = pd.DataFrame({"CreditorGLN": [cred_gln_no],
                       "InvoiceNum": [inv_no],
                       "Barcode": [barcodes],
                       "ProductNameFSC": [names_and_fsc]})
    df = df.explode(["Barcode", "ProductNameFSC"]).reset_index(drop=True)
    return df


def parse_xml_files(files: list) -> pd.DataFrame:
    """
    Top-level function to parse xml files.
    Returns a dataframe based on input files.
    """
    list_of_dfs = []
    for file in files:
        try:
            df = make_df_from_xml_file(file)
            list_of_dfs.append(df)
        except Exception:
            pass

    stacked_df = pd.concat(list_of_dfs)
    return stacked_df



xml_file = "files/Burde invoice_000759106_2021-08-11-10-45-31{c732b041-f0d5-483e-b83b-3b92722a3b59}.xml"
files = [xml_file]

data = parse_xml_files(files)


# item descriptions - w/ FSC
#items_descriptions = [i.Description.text for i in items]


# Item ID - barcodes
# We use a for loop since values can be None and cause an attribute error
#barcodes = [i.ID.text for i in items]
#barcodes = []
#for i in items:
#    try:
#        barcodes.append(i.ID.text)
#    except:
#        barcodes.append("")

#with open(xml_file, 'r') as file:
#    xml_string = file.read().replace('\n', '')
