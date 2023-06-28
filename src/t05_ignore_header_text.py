"""
header_textを人力で定めるのは恣意的と言われそうなので、いったん保留
first_lineをtextとマージしたjsonを返すだけのスクリプト
"""
import glob
import os
import csv
from typing import List, Tuple, Dict, Set,Optional
import re
import json

def export_to_json(filename:str,contents)->None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump({
            "contents":contents
        }, f, ensure_ascii=False, indent=2)

def main_func(data):
    res=[]
    for content in data["contents"]:
        res.append({
            "type":content["type"],
            "header":content["header"],
            "text":content["first_line"]+content["text"]
        })
    return res
def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        contents=json.load(contents)
        contents=main_func(contents)
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json",contents)

if __name__=="__main__":
    main("./04","./05")