# -*- coding: UTF-8 -*

from bs4 import BeautifulSoup as bs4
import pandas as pd
import re
import os

path = "files"
file_names = os.listdir(path)
files = [os.path.join(path,i) for i in file_names]

def parse_all_files(files: list) -> pd.DataFrame:
    """
    Top-level function to parse both .edi and .xml files.
    Returns a dataframe with key data from input files.
    """
    edi_files = [i for i in files if i.endswith('.edi')]
    xml_files = [i for i in files if i.endswith('.xml')]

    list_of_dfs = []
    if len(edi_files) > 0:
        edi_data = parse_edi_files(edi_files)
        list_of_dfs.append(edi_data)
    if len(xml_files) > 0:
        xml_data = parse_xml_files(xml_files)
        list_of_dfs.append(xml_data)

    stacked_df = pd.concat(list_of_dfs)

    stacked_df = stacked_df[stacked_df['ProductNameFSC'].str.contains("FSC")]
    stacked_df['FSCValue'] = stacked_df['ProductNameFSC'].str.findall('FSC.*').apply(','.join)

    return stacked_df


final_df = parse_all_files(files)
final_df.astype(str).to_csv("FSC_output_test.csv", index=False, sep=";", encoding="latin-1")



# create excel writer object
writer = pd.ExcelWriter('FSC_output_test.xlsx')
# write dataframe to excel
final_df.astype(str).to_excel(writer)
# save the excel
writer.save()