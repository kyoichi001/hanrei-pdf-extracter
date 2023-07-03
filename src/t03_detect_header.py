"""
ヘッダー候補を抽出


スペースの混じった文をヘッダー候補として抽出
一文字ごとにスペースがある場合はまた別の処理が必要・・・

"""


import csv
from typing import List, Tuple, Dict, Set,Optional,Final,TypedDict
import re
import json

class Section(TypedDict):
    header:str
    texts:list[str]
class Chapter(TypedDict):
    header_text:str
    sections:list[Section]
class Hanrei(TypedDict):
    signature:Chapter
    judgement:Chapter
    main_text:Chapter
    fact_reason:Chapter

def export_to_json(filename:str,data:Hanrei)->None:
    obj={
        "contents":data
    }
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def main_func(texts:List[str])->Hanrei:
    text:Section={"header":"","texts":[]}
    res:Hanrei={
        "signature":{"header_text":"","sections":[]},
        "judgement":{"header_text":"","sections":[]},
        "main_text":{"header_text":"","sections":[]},
        "fact_reason":{"header_text":"","sections":[]},
    }
    res_obj:list[Section]=[]
    main_section_headers:Final=["判決","主文","事実及び理由"]
    current_phase=0
    header_file = open("./rules/headers.json", "r", encoding="utf-8")
    headers_obj=json.load(header_file)
    header_others=[rule for rule in headers_obj["rules"] if "order" in rule and rule["order"]==False]
    count=0
    for t in texts:
        t_=t.replace(" ","").replace("\t","").replace("　","")
        if t_ in main_section_headers:# 主文、事実及び理由の場合
            res_obj.append(text)
            if current_phase==0:
                res["signature"]={"header_text":"","sections":res_obj[:]}
            elif current_phase==1:
                res["judgement"]={"header_text":"判決","sections":res_obj[:]}
            elif current_phase==2:
                res["main_text"]={"header_text":"主文","sections":res_obj[:]}
            text={"header":"","texts":[]}
            res_obj=[]
            current_phase+=1
            continue
        header_flg=False
        for h in header_others:
            if re.fullmatch(f"^{h['regex']}",t_) is not None:#〔被告の主張〕などにマッチしたら
                if len(text["header"])>0:res_obj.append(text)
                text={"header":t_,"texts":[]}
                header_flg=True
                break
        if header_flg:continue
        aaaaa=t.split()
        if len(aaaaa)>=2:#スペースで区切れる場合、（暫定）セクションとしておく
            if len(text["header"])>0:res_obj.append(text)
            text={"header":aaaaa[0],"texts":["".join(aaaaa[1:])]}
        else:
            text["texts"].append(t)
        count+=1
    res_obj.append(text)
    res["fact_reason"]={"header_text":"事実及び理由","sections":res_obj[:]}
    return res
            
import glob
import os

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")

    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        data:list=json.load(contents)["contents"]
        print(f"入力 {len(data)}行")
        container=main_func(data)
        output_path=os.path.splitext(os.path.basename(file))[0]
        print(f"出力 {len(container)}行")
        export_to_json(f"{outputDir}/{output_path}.json",container)

if __name__=="__main__":
    main("./02","./03")