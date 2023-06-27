"""
ヘッダー候補を抽出


スペースの混じった文をヘッダー候補として抽出
一文字ごとにスペースがある場合はまた別の処理が必要・・・

"""


import csv
from typing import List, Tuple, Dict, Set,Optional
import re
import json

def export_to_json(filename:str,data)->None:
    obj={
        "contents":data
    }
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def main_func(texts:List[str]):
    text={"header":"","texts":[]}
    res=[]
    main_section_headers=["判決","判 決","主文","主 文","事実及び理由","事 実 及 び 理 由","事  実  及  び  理  由"]
    header_file = open("./headers.json", "r", encoding="utf-8")
    headers_obj=json.load(header_file)
    header_others=[rule for rule in headers_obj["rules"] if "order" in rule and rule["order"]==False]
    header_text=""
    print(header_others)
    count=0
    for t in texts:
        if t in main_section_headers:# 主文、事実及び理由の場合
            res.append(text)
            text={"header":t.replace(" ",""),"texts":[]}
            continue
        header_flg=False
        for h in header_others:
            if re.fullmatch(f"^{h['regex']}",t) is not None:#〔被告の主張〕などにマッチしたら
                res.append(text)
                text={"header":t.replace(" ",""),"texts":[]}
                header_flg=True
                break
        if header_flg:continue
        aaaaa=t.split()
        if len(aaaaa)>=2:#スペースで区切れる場合、（暫定）セクションとしておく
            #print(aaaaa)
            res.append(text)
            text={"header":aaaaa[0],"texts":["".join(aaaaa[1:])]}
        else:
            text["texts"].append(t)
        count+=1
    return [i for i in res if i["header"]!=""]
            
import glob
import os

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")

    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        contents=json.load(contents)["contents"]
        print(f"入力 {len(contents)}行")
        container=main_func(contents)
        output_path=os.path.splitext(os.path.basename(file))[0]
        print(f"出力 {len(container)}行")
        export_to_json(f"{outputDir}/{output_path}.json",container)

if __name__=="__main__":
    main("./02","./03")