import string
import os
from datetime import datetime


def clean_string(s):
    return s.translate(str.maketrans('', '', string.punctuation))


def convert_to_date(s):
    date = s[2: -4]
    formatStr = "%y%m%d"
    date = datetime.strptime(date, formatStr)
    return date


def get_all_text_files_in_dir(rootPath):
    ret = set()
    for d in os.walk(rootPath):
        for f in d[2]:
            ret.add(os.path.join(d[0], f))
    return ret
        
if __name__ == "__main__":
    files = get_all_text_files_in_dir("data/all/")
    if files is not None:
        for f in files:
            print(f)
