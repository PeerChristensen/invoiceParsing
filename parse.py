from typing import List

import pandas as pd

from xml_parser import XMLParser
from edi_parser import EDIParser


file_parser_map = {
    "xml": XMLParser,
    "edi": EDIParser,
}


def parse_files(file_names: List[str]) -> pd.DataFrame:

    list_of_dfs = []
    for file_name in file_names:
        extension = file_name.split(".")[-1]
        if extension not in file_parser_map:
            raise ValueError(
                f"Extension {extension} not supported. Valid extensions are {list(file_parser_map.keys())}"
            )
        df = file_parser_map[extension](file_name).parse()
        if "/" in file_name:
            file_name = file_name.split("/")[-1]
        df["Filename"] = file_name
        list_of_dfs.append(df)
    stacked_df = pd.concat(list_of_dfs)
    stacked_df = stacked_df[stacked_df['ProductNameFSC'].str.contains("FSC")]
    stacked_df['FSCValue'] = stacked_df['ProductNameFSC'].str.findall('FSC.*').apply(','.join)
    stacked_df = stacked_df[['Filename'] + [col for col in stacked_df.columns if col != 'Filename']]
    return stacked_df




