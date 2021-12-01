
from parse import parse_files
import os
from glob import glob

#------------------------------------------------------------
# PARSE ALL
#------------------------------------------------------------

#path = "files"
#file_names = os.listdir(path)
#files = [os.path.join(path, i) for i in file_names]

glob_pattern = os.path.join('many_files', '*')
file_names = glob(glob_pattern)

df = parse_files(file_names)
df.head()

"""for i in file_names:
    print(f"\n\n\n\n\n\n{i}")
    df = parse_files([i])
    print(f"\n{df}")"""

df.to_csv("data/FSC_output_more_features_large.csv", sep=",", index=False)


