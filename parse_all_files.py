from bs4 import BeautifulSoup as bs4
import pandas as pd
import re
import os

path = "files"
file_names = os.listdir(path)
files = [os.path.join(path,i) for i in file_names]

def parse_all_files(files: list) -> pd.DataFrame:

    edi_files = [i for i in files if i.endswith('.edi')]
    xml_files = [i for i in files if i.endswith('.xml')]

    edi_data = parse_edi_files(edi_files)
    xml_data = parse_xml_files(xml_files)

    list_of_dfs = [edi_data, xml_data]

    stacked_df = pd.concat(list_of_dfs)
    return stacked_df

final_df = parse_all_files(files)
