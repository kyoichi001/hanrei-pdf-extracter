"""
t06_split_centenceの出力データから、行数、文の平均長、最大、最小長を算出します
"""
import glob
import os
import csv
from typing import List, Tuple, Dict, Set, Optional
import re
import json
from typing import List, Tuple, Dict, Set
import re

def analyze(filepath):
    len_ave=0
    len_min=1000000000
    len_max=0
    sentence_count=0
    with open(filepath, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            #print(row)
            text=row[3]
            if text=="" or text is None or text=="_":continue
            #if len(text)<=3:
                #print(row)
            sentence_count+=1
            len_ave+=len(text)
            if len_min>len(text):len_min=len(text)
            if len_max<len(text):len_max=len(text)
    return {
        "ave":len_ave/sentence_count,
        "min":len_min,
        "max":len_max,
        "count":sentence_count,
    }

def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.csv")

    for file in files:
        print(file)
        res=analyze(file)
        print(res)

if __name__ == "__main__":
    main("./06", "./06")
