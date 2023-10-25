# 時間表現を含む文をフィルタリング

import glob
import os
import csv
from typing import List, Tuple, Dict, Set, Optional,Union,Any
import re
import json
import re

def filter_text(text:str,rule)->bool:
    for r in rule["point"]:
        regex=r["regex"]
        a = re.search(regex, text)
        if a is not None:
            return True
    return False

def export_to_csv(filename: str, data,rule) -> None:
    res:Any={
        "signature":data["contents"]["signature"],
        "judgement":data["contents"]["judgement"],
        "main_text":{},
        "fact_reason":{},
    }
    main_text=data["contents"]["main_text"]
    fact_reason=data["contents"]["fact_reason"]
    csv_result:list[list[Union[int,str]]] = [["id", "text_id","content"]]
    text_id = 0
    for t in main_text["sections"]:
        #print(t)
        if "texts" in t:
            for text in t["texts"]:
                t=text["text"]
                if filter_text(t,rule):
                    csv_result.append([text_id,text["text_id"],t])
                    text_id+=1
        else:
            print("👺予期しないエラー")
            print(t)
        if "blackets" in t:
            for text in t["blackets"]:
                t=text["content"]
                if filter_text(t,rule):
                    csv_result.append([text_id,text["text_id"],t])
                    text_id+=1
        if "selifs" in t:
            for text in t["selifs"]:
                t=text["content"]
                if filter_text(t,rule):
                    csv_result.append([text_id,text["text_id"],t])
                    text_id+=1
    for t in fact_reason["sections"]:
        #print(t)
        if "texts" in t:
            for text in t["texts"]:
                t=text["text"]
                if filter_text(t,rule):
                    csv_result.append([text_id,text["text_id"],t])
                    text_id+=1
        else:
            print("👺予期しないエラー")
            print(t)
        if "blackets" in t:
            for text in t["blackets"]:
                t=text["content"]
                if filter_text(t,rule):
                    csv_result.append([text_id,text["text_id"],t])
                    text_id+=1
        if "selifs" in t:
            for text in t["selifs"]:
                t=text["content"]
                if filter_text(t,rule):
                    csv_result.append([text_id,text["text_id"],t])
                    text_id+=1

    import csv

    with open(filename+".csv", 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in csv_result:
            writer.writerow(row)
            

def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")

    rule_data = open("./rules/time_rules.json", "r", encoding="utf-8")
    rule_data = json.load(rule_data)

    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        contents = json.load(contents)
        # print(contents)
        #print(f"入力 {len(contents)}行")
        output_path = os.path.splitext(os.path.basename(file))[0]
        #print(f"出力 {len(container)}行")
        export_to_csv(f"{outputDir}/{output_path}", contents,rule_data)
if __name__ == "__main__":
    main("./06", "./07")