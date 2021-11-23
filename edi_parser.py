import re
import pandas as pd


class EDIParser:

    def __init__(self, file_name: str):
        self.content_list = self.get_edi_content(file_name)

    @staticmethod
    def get_edi_content(file_name) -> list:
        """Read content and split on "'". Returns a list"""
        content = open(file_name, "r", encoding="latin1").read()
        content_list = content.split("'")
        return content_list

    def get_creditor_gln(self) -> str:
        """
        Get Creditor GLN from edifact file
        Q: Does the relevant element always start with "UNB+UNOC:3+
        Q: Is this the same as Creditor number"
        """
        for i in self.content_list:
            if i.startswith('UNB+UNOC'):
                creditor_gln__string = i
                break

        creditor_gln = re.search('UNB\\+UNOC:3\\+(.*?)\\:', creditor_gln__string).group(1)
        return creditor_gln

    def get_invoice_no(self) -> str:
        """Get invoice number from edifact file"""
        invoice_string = None
        for i in self.content_list:
            if i.startswith('BGM+380+'):
                invoice_string = i
                break

        if invoice_string:
            return re.search('BGM\\+380\\+(.*?)\\+9', invoice_string).group(1)
        else:
            return ""

    def get_barcodes(self) -> list:
        """Get list of barcodes from edifact file"""
        barcode_lines = [i for i in self.content_list if i.startswith("LIN")]
        barcodes = []
        for line in barcode_lines:
            try:
                barcode = re.search('\\+\\+(.*?)\\:', line).group(1)
                barcodes.append(barcode)
            except AttributeError:
                pass
        if len(barcodes) == 0:
            return [""]
        return barcodes

    def get_name_and_fsc(self) -> list:
        """Get product name/description and FSC info"""
        name_and_fsc_lines = [i for i in self.content_list if i.startswith("IMD+F+")]
        name_and_fsc_list = []
        for line in name_and_fsc_lines:
            name_and_fsc = re.search(':::(.*)', line).group(1)
            name_and_fsc_list.append(name_and_fsc)

        if len(name_and_fsc_list) == 0:
            return [""]
        return name_and_fsc_list

    def parse(self) -> pd.DataFrame:
        """Main function  that parses EDI."""
        df = pd.DataFrame({"CreditorGLN": [self.get_creditor_gln()],
                           "InvoiceNum": [self.get_invoice_no()],
                           "Barcode": [self.get_barcodes()],
                           "ProductNameFSC": [self.get_name_and_fsc()]})
        return df.explode(["Barcode", "ProductNameFSC"]).reset_index(drop=True)


p = EDIParser("many_files/20200916_120003375_55.edi")
p = EDIParser("files/Staedtler Nordic AS_20210519_040021930_26.edi")
df = p.parse()
df.explode(["Barcode", "ProductNameFSC"]).reset_index(drop=True)