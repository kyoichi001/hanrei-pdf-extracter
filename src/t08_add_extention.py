import glob
import os
import csv
from typing import List, Tuple, Dict, Set, Optional,Final,Union,Any
import re
import json
import re


"""
争点 + 数字という表現があれば、そのセクションはその争点に属すると判定
複数含まれる場合、本文よりもヘッダーテキストが優先、はじめに登場したものが優先される
"""

def sanitize(text:str)->str:
    d=["１","1","２","2","３","3","４","4","５","5","６","6","７","7","８","8","９","9","０","0"]
    for i in range(10):
        text=text.replace(d[i*2],d[i*2+1])
    return text

def has_issue_expression(text:str)->Optional[int]:
    text=sanitize(text)
    a = re.search(r"争点(?P<num>\d+)", text)
    if a is None: return None
    count = a.groupdict().get("num")
    if count is None:return None
    return int(count)
def has_claim_expression(text:str,indent:int)->Optional[str]:
    if text.find("主張")!=-1:
        if text.find("原告")!=-1:return "genkoku"
        if text.find("被告")!=-1:return "hikoku"
    if text.find("判断")!=-1 and indent==1:return "saibanjo"
    return None

def main_func(data):
    res:Any={
        "signature":data["contents"]["signature"],
        "judgement":data["contents"]["judgement"],
        "main_text":data["contents"]["main_text"],
        "fact_reason":{},
    }
    fact_reason=data["contents"]["fact_reason"]
    issue_indent=None
    bef_issue_num=None
    claim_indent=None
    bef_claim_state=None
    for t in fact_reason["sections"]:
        #texts=t["texts"]
        indent=t["indent"]
        header=t["header"]
        header_text=t["header_text"]
        issue_num=has_issue_expression(header_text)
        claim_state=None
        claim_state1=has_claim_expression(header,indent)
        claim_state2=has_claim_expression(header_text,indent)
        if issue_num is not None:
            issue_indent=indent
            bef_issue_num=issue_num
        if claim_state1 is not None or claim_state2 is not None:
            claim_indent=indent
            if claim_state1 is not None:claim_state=claim_state1
            if claim_state2 is not None:claim_state=claim_state2
            bef_claim_state=claim_state
        if issue_num is None and issue_indent is not None:
            if indent>issue_indent:
                issue_num=bef_issue_num
            else:
                bef_issue_num=None
                issue_indent=None
        if claim_state is None and claim_indent is not None:
            if indent>claim_indent:
                claim_state=bef_claim_state
            else:
                bef_claim_state=None
                claim_indent=None
        if issue_num is not None:t["issue_num"]=issue_num
        if claim_state is not None:t["claim_state"]=claim_state
    res["fact_reason"]=fact_reason
    return res

def export_to_csv(filename:str,data)-> None:
    csv_result:list[list[Union[int,str]]] = [["id", "header", "header_text","issue","claim","content"]]
    for section in data["fact_reason"]["sections"]:
        if "texts" not in section:
            csv_result.append(["",section["header"],section["header_text"],section.get("issue_num"),section.get("claim_state"),""])
        else:
            for text in section["texts"]:
                csv_result.append([text["text_id"],section["header"],section["header_text"],section.get("issue_num"),section.get("claim_state"),text["text"]])
    import csv
    with open(filename+".csv", 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in csv_result:
            writer.writerow(row)

def export_to_json(filename: str, data) -> None:
    with open(filename+".json", 'w', encoding='utf8', newline='') as f:
        json.dump({"contents":data}, f, ensure_ascii=False, indent=2)

def main(inputDir: str, outputDir: str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")

    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        contents = json.load(contents)
        # print(contents)
        #print(f"入力 {len(contents)}行")
        output_path = os.path.splitext(os.path.basename(file))[0]
        #print(f"出力 {len(container)}行")
        res=main_func(contents)
        export_to_csv(f"{outputDir}/{output_path}", res)
        export_to_json(f"{outputDir}/{output_path}", res)


if __name__ == "__main__":
    main("./06", "./08")
