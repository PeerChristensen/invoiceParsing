import re
import pandas as pd


def get_edi_content(file: str) -> list:
    """Read content and split on "'". Returns a list"""
    content = open(file, "r", encoding="latin1").read()
    content_list = content.split("'")
    return content_list


def get_creditor_gln(content: list) -> str:
    """
    Get Creditor GLN from edifact file
    Q: Does the relevant element always start with "UNB+UNOC:3+
    Q: Is this the same as Creditor number"
    """
    for i in content:
        if i.startswith('UNB+UNOC'):
            creditor_gln__string = i
            break

    creditor_gln = re.search('UNB\\+UNOC:3\\+(.*?)\\:', creditor_gln__string).group(1)
    return creditor_gln


def get_invoice_no(content: list) -> str:
    """Get invoice number from edifact file"""
    for i in content:
        if i.startswith('BGM+380+'):
            invoice_string = i
            break

    invoice_no = re.search('BGM\\+380\\+(.*?)\\+9', invoice_string).group(1)
    return invoice_no


def get_barcodes(content: list) -> list:
    """Get list of barcodes from edifact file"""
    barcode_lines = [i for i in content if i.startswith("LIN")]
    barcodes = []
    for line in barcode_lines:
        barcode = re.search('\\+\\+(.*?)\\:', line).group(1)
        barcodes.append(barcode)

    return barcodes


def get_name_and_fsc(content: list) -> list:
    """Get product name/description and FSC info"""
    name_and_fsc_lines = [i for i in content if i.startswith("IMD+F+")]
    name_and_fsc_list = []
    for line in name_and_fsc_lines:
        name_and_fsc = re.search(':::(.*)', line).group(1)
        name_and_fsc_list.append(name_and_fsc)

    return name_and_fsc_list


def make_df_from_edi_file(file: str) -> pd.DataFrame:
    """
    This function calls various helper functions to create a dataframe after parsing
    the relevant content from .edi files.
    """
    content = get_edi_content(file)            # get content
    cred_gln_no = get_creditor_gln(content)    # get creditor GLN number
    inv_no = get_invoice_no(content)           # get invoice number
    barcodes = get_barcodes(content)           # get barcodes
    names_and_fsc = get_name_and_fsc(content)  # get names and FSC codes

    df = pd.DataFrame({"CreditorGLN": [cred_gln_no],
                       "InvoiceNum": [inv_no],
                       "Barcode": [barcodes],
                       "ProductNameFSC": [names_and_fsc]})
    df = df.explode(["Barcode", "ProductNameFSC"]).reset_index(drop=True)
    return df


def parse_edi_files(files: list) -> pd.DataFrame:
    """
    Top-level function to parse edifact files.
    Returns a dataframe based on input files.
    """
    list_of_dfs = []
    for file in files:
        try:
            df = make_df_from_edi_file(file)
            list_of_dfs.append(df)
        except Exception:
            pass

    stacked_df = pd.concat(list_of_dfs)
    return stacked_df

