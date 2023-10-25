"""

セルをx,y座標で並び替える
y座標が同じなら結合

"""

import csv
from typing import List, Tuple, Dict, Set,Optional,Any
import re
import json
import t01_type
import t02_type

def export_to_json(filename:str,data:List[str])->None:
    obj={
        "header":{
            "texts_count":len(data)
        },
        "contents":data
    }
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def clean_text(txt:str)->str:
    return txt.strip().replace('\n', '').replace('\t', '').replace("（","(").replace("）",")")

def main_func(data:t01_type.Page)->list[str]:
    #yが小さい順（上から下）にソート
    res = sorted(data["contents"],key=lambda x: (-x["y"],x["x"]))
    if len(res)==1:#行番号やページ番号を除外したものを返す
        return [clean_text(i["text"]) for i in res if clean_text(i["text"])!="" and re.match('^[-ー \d]+$', i["text"]) == None]
    i=1
    while i<len(res):#同じy座標にあるテキストを結合
        if res[i-1]["y"]==res[i]["y"]:
            #print("!!!!!!!!!!!!",res[i-1]["text"],res[i]["text"])
            res[i-1]["text"]+=res[i]["text"]
            res.pop(i)
            continue
        i+=1

    return [clean_text(i["text"]) for i in res if clean_text(i["text"])!="" and re.match('^[-ー \d]+$', i["text"]) == None]
            
import glob
import os

def main(data):
    pages:List[t01_type.Page]=data["pages"]
    #print(f"入力 {len(contents)}行")
    output:list[str]=[]
    for page in pages:
        output.extend(main_func(page))
    return {
        "header":{
            "texts_count":len(output)
        },
        "contents":output
    }