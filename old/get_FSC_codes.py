
from glob import glob
import os
import pandas as pd
from bs4 import BeautifulSoup as bs4
from xml_parser import XMLParser
from edi_parser import EDIParser

# ------------------------------------
# XML
# ------------------------------------

glob_pattern = os.path.join('../files', '*xml')
file_name = glob(glob_pattern)[0]

content = XMLParser.get_xml_content(file_name)

def get_issue_date_xml(content) -> str:
    """Get issue date from xml file"""
    issue_date = content.find("cbc:IssueDate").text
    return issue_date


date = get_issue_date_xml(content)


def get_fsc_code_xml(content) -> str:
    """Get FSC code from xml file"""
    note_with_fsc_list = content.find("cbc:Note").text.split(".")
    for i in note_with_fsc_list:
        if "COC" in i:
            fsc_code_string = i
            break
    fsc_code = fsc_code_string.split(":")[1].strip()
    return fsc_code

fsc_code = get_fsc_code_xml(content)

# ------------------------------------
# EDI
# ------------------------------------

glob_pattern = os.path.join('../files', '*edi')
file_name = glob(glob_pattern)[1]

content = EDIParser.get_edi_content(file_name)


def get_issue_date(content) -> str:
    """Get issue date from edi file"""
    issue_date = None
    for string in content:
        if "DTM" in string.upper():
            issue_date = string.split(":")[1]
            break

    if issue_date:
        return issue_date
    else:
        return ""


def get_fsc_code(content) -> str:
    """Get FSC code from edi file"""

    fsc_code = None
    for string in content:
        if "COC" in string.upper():
            coc_string = string.upper().split(" ")
            for substring in coc_string:
                if "COC" in substring:
                    fsc_code = substring
                    break

    if fsc_code:
        return fsc_code
    else:
        return ""


fsc_code = get_fsc_code(content)