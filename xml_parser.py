from typing import List
from bs4 import BeautifulSoup as bs4
import pandas as pd


class XMLParser:

    def __init__(self, file_name: str):
        self.soup = self.get_xml_content(file_name)

    @staticmethod
    def get_xml_content(file_name) -> bs4:
        """
        Read content from an xml file.
        Returns a 'BeautifulSoup object'
        """
        content = open(file_name, "r", encoding="utf8").read()
        soup = bs4(content, "xml")
        return soup

    def get_issue_date_xml(self) -> str:
        """Get issue date from xml file"""
        issue_date = None
        issue_date = self.soup.find("cbc:IssueDate").text
        if issue_date:
            return issue_date
        else:
            return ""

    def get_creditor_gln_xml(self) -> str:
        """Get Creditor GLN from xml file"""
        acp_tag = self.soup.find("cac:AccountingCustomerParty")
        creditor_gln = acp_tag.PartyIdentification.ID.text
        return creditor_gln

    def get_fsc_code_xml(self) -> str:
        """Get FSC code from xml file"""
        fsc_code = None
        note_with_fsc_list = self.soup.find("cbc:Note").text.split(".")
        for i in note_with_fsc_list:
            if "COC" in i.upper():
                fsc_code_string = i
                break
        if fsc_code_string:
            fsc_code = fsc_code_string.split(":")[1].strip()
            return fsc_code
        else:
            return fsc_code

    def get_invoice_no_xml(self) -> str:
        """Get invoice number from xml file"""
        invoice_no = self.soup.find("cbc:ID").text
        return invoice_no

    def get_items_xml(self) -> bs4:
        """Get all 'Item' tags from xml"""
        items = self.soup.findAll("cac:Item")
        return items

    def get_barcodes_xml(self) -> list:
        """Get list of barcodes from xml file"""
        barcodes = []
        for i in self.get_items_xml():
            try:
                barcodes.append(i.ID.text)
            except:
                barcodes.append("")
        return barcodes

    def get_name_and_fsc_xml(self) -> list:
        """Get product name/description and FSC info"""
        items_descriptions = []
        for i in self.get_items_xml():
            try:
                items_descriptions.append(i.Description.text)
            except:
                items_descriptions.append("")
        return items_descriptions

    def parse(self) -> pd.DataFrame:
        """Main function  that parses XML."""

        df = pd.DataFrame({"IssueDate": [self.get_issue_date_xml()],
                            "CreditorGLN": [self.get_creditor_gln_xml()],
                           "FSCCode": [self.get_fsc_code_xml()],
                           "InvoiceNum": [self.get_invoice_no_xml()],
                           "Barcode": [self.get_barcodes_xml()],
                           "ProductNameFSC": [self.get_name_and_fsc_xml()]})
        return df.explode(["Barcode", "ProductNameFSC"]).reset_index(drop=True)


'''
file_parser_map = {
    "xml": XMLParser,
}


def parse_xml_files(file_names: List[str]) -> pd.DataFrame:

    list_of_dfs = []
    for file_name in file_names:
        extension = file_name.split(".")[-1]
        df = file_parser_map[extension](file_name).parse()
        list_of_dfs.append(df)

    stacked_df = pd.concat(list_of_dfs)
    return stacked_df
'''