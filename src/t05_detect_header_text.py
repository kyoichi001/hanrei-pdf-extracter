"""
first_lineがheader_textであるかどうかを手動で指定する

header, first_lineとそれに続くtextが与えられ、これはheader_textか？と聞かれるので、
y/n
で答える
"""

import glob
import os
import csv
from typing import List, Tuple, Dict, Set,Optional,Any
import re
import json

def blacket_level(str:str)->int:
    """
    
    """
    level=0
    for i in str:
        if i=="(" or i=="[" or i=="（" or i=="「":level+=1
        if i==")" or i=="]" or i=="）" or i=="」":level-=1
    return level

def split_blacket(str1:str,str2:str,level:int):
    """

    """
    str2=re.sub(r"([)\]）」])",r'\1#',str2)
    ls=str2.split("#")
    print("ls :",ls)
    return str1+"".join(ls[:level]),"".join(ls[level:])

def main_func(data)->Tuple[Any,List[str]]:
    res:Any={
        "signature":data["contents"]["signature"],
        "judgement":data["contents"]["judgement"],
        "main_text":{},
        "fact_reason":{},
    }
    main_text_res={
        "header_text":data["contents"]["main_text"]["header_text"],
        "sections":[]
    }
    for section in data["contents"]["main_text"]["sections"]:
        text="".join(section["texts"])
        main_text_res["sections"].append({
          "type": section["type"],
          "header": section["header"],
          "text": text,
          "indent": section["indent"],
        })
    data_count=len(data["contents"]["fact_reason"]["sections"])
    res_obj:List[Any]=[{} for i in range(data_count)]
    answers:List[str]=["" for i in range(data_count)]
    index=0
    while index<data_count:
        c=data["contents"]["fact_reason"]["sections"][index]
        if c["type"]=="":
            index+=1
            continue
        flag=""
        header=c["header"]
        first_line=""
        text=""
        if len(c["texts"])>0:
            first_line=c["texts"][0]
        if len(c["texts"])>1:
            text="".join(c["texts"][1:])
        lv=blacket_level(first_line)
        if lv!=0:
            first_line,text=split_blacket(first_line,text,lv)
        while True:
            print(f"================== {index} / {data_count} =========================")
            print("header:     ",header)
            print("first_line: ",first_line)
            print("text:       ",text)
            ans = input("これはheader_text? (y(yes) Y(yes(first_line+text)) / n(no) / u(undo))")
            if ans=="y" or ans=="Y" or ans=="n" or ans=="u":
                flag=ans
                break
            else:
                print("error やり直し")
        obj={}
        if flag=="y":
            obj={
                "type": c["type"],
                "header": header,
                "header_text":first_line,
                "text":text,
                "indent":c["indent"]
            }
        elif flag=="Y":
            obj={
                "type": c["type"],
                "header": header,
                "header_text":first_line+text,
                "text":"",
                "indent":c["indent"]
            }
        elif flag=="n":
            obj={
                "type": c["type"],
                "header": header,
                "header_text":"",
                "text":first_line+text,
                "indent":c["indent"]
            }
        elif flag=="u":
            index-=1
            continue
        res_obj[index]=obj
        answers[index]=flag
        index+=1
    res["main_text"]=main_text_res
    res["fact_reason"]={
        "header_text":data["contents"]["fact_reason"]["header_text"],
        "sections":res_obj
    }
    return res,answers

def export_to_json(filename:str,contents,answers:List[str])->None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump({
            "contents":contents
        }, f, ensure_ascii=False, indent=2)

    import csv

    with open(filename+"_answers.csv", 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in answers:
            if row=="":continue # c["type"]=="" のとき飛ばされた列を無視
            writer.writerow(row)

    with open(filename+"_texts.csv", 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id","header","header_text","text"])
        id=0
        for content in contents["fact_reason"]["sections"]:
            writer.writerow([id,content["header"],content["header_text"],content["text"]])
            id+=1
    
    

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")
    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        contents=json.load(contents)
        contents,answers=main_func(contents)
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"{outputDir}/{output_path}.json",contents,answers)

if __name__=="__main__":
    main("./04","./05")