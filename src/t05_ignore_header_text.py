"""
header_textを人力で定めるのは恣意的と言われそうなので、いったん保留
first_lineをtextとマージしたjsonを返すだけのスクリプト
"""
import glob
import os
import csv
from typing import List, Tuple, Dict, Set,Optional,Any
import re
import json

def export_to_json(filename:str,contents)->None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump({
            "contents":contents
        }, f, ensure_ascii=False, indent=2)

def main_func(data):
    res:Any={
        "signature":data["contents"]["signature"],
        "judgement":data["contents"]["judgement"],
        "main_text":{},
        "fact_reason":{},
    }
    main_text=data["contents"]["main_text"]
    fact_reason=data["contents"]["fact_reason"]
    res_obj=[]
    for content in main_text["sections"]:
        res_obj.append({
            "type":content["type"],
            "header":content["header"],
            "header_text":"",
            "text":"".join(content["texts"])
        })
    res["main_text"]={
        "header_text":data["contents"]["main_text"]["header_text"],
        "sections":res_obj
    }
    res_obj=[]
    for content in fact_reason["sections"]:
        res_obj.append({
            "type":content["type"],
            "header":content["header"],
            "header_text":"",
            "text":"".join(content["texts"])
        })
    res["fact_reason"]={
        "header_text":data["contents"]["fact_reason"]["header_text"],
        "sections":res_obj
    }
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