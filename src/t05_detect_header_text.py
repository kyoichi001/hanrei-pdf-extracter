"""
first_lineがheader_textであるかどうかを手動で指定する

header, first_lineとそれに続くtextが与えられ、これはheader_textか？と聞かれるので、
y/n
で答える
"""

import glob
import os
import csv
from typing import List, Tuple, Dict, Set,Optional
import re
import json

def blacket_level(str:str)->bool:
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

def main_func(data):
    res=[]
    for content in data["contents"]:
        if content["type"]=="":continue
        flag=False
        header=content["header"]
        first_line=content["first_line"]
        text=content["text"]
        lv=blacket_level(first_line)
        if lv!=0:
            first_line,text=split_blacket(first_line,text,lv)
        while True:
            print("===========================================")
            print("header:     ",header)
            print("first_line: ",first_line)
            print("text:       ",text)
            ans = input("これはheader_text? (y/n)")
            if ans=="y":
                flag=True
                break
            elif ans=="n":
                flag=False
                break
            else:
                print("error やり直し")
        obj={}
        if flag:
            obj={
                "type": content["type"],
                "header": header,
                "header_text":first_line,
                "text":text
            }
        else:
            obj={
                "type": content["type"],
                "header": header,
                "header_text":"",
                "text":first_line+text
            }
        res.append(obj)
    return res

def export_to_json(filename:str,contents)->None:
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump({
            "contents":contents
        }, f, ensure_ascii=False, indent=2)

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