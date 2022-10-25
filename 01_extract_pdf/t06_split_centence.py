import csv
from typing import List, Tuple, Dict, Set,Optional
import re
import json
from typing import List, Tuple, Dict, Set
import re

def split_text(text:str)->List[str]:
    a=re.sub("。([^」\\)〕])","。$\\1",text)
    texts_dat=a.split("$")
    if len(texts_dat)==0:return text
    return texts_dat

def extract_kakko(text:str)->List[str]:
    """
    カッコの入っている文からカッコとそれ以外を抽出
    """
    count=0
    res_wokakko=""
    res_kakko=""
    res=[]
    if text=="":return [""]
    if text[0]=="(" or text[0]=="「":count=1
    if count>=1:res_kakko+=text[0]
    else: res_wokakko+=text[0]
    for i in range(1,len(text)):
        if text[i-1]==")" or text[i-1]=="」":
            count-=1
            if count==0:
                res.append(res_kakko)
                res_kakko=""
        if text[i]=="(" or text[i]=="「":
            count+=1
            if count==1:
                res.append(res_wokakko)
                res_wokakko=""
        if count>=1:res_kakko+=text[i]
        else: res_wokakko+=text[i]
    if count>=1: res.append(res_kakko)
    else: res.append(res_wokakko)
    return [i for i in res if i !=""]

def split_texts(text:str)->List[str]:
    texts=extract_kakko(text)#文からカッコとそうでないのを区切る。配列を返す
    texts2:List[str]=[]
    for txt in texts:
        if txt=="":continue
        if txt[0]=="(" or txt[0]=="「":#そのテキストが「」・（）の形式の文だったら、「。」で区切らない
            texts2.append(txt)
            continue
        for i in split_text(txt):#「。」で区切る
            if i=="":continue
            texts2.append(i)
    return texts2

def text_to_data(inputs:list[str]):
    """
    一文からselifsやblacketsなどのデータを返す
    """
    selifs=[]
    blackets=[]
    text=""
    current_selif_count=0
    for input in inputs:
        if input[0]=="「":
            selifs.append({
                "target_selif":current_selif_count, #その文の何番目の「セリフ」を置換するか
                "content":input
            })
            current_selif_count+=1
            text+="「セリフ」"
        elif input[0]=="(" or input[0]=="（":
            blackets.append({
                "position":len(text), #何文字目の前に埋め込むか（0なら最初の文字の前に埋め込む）
                "content":input,
            })
        else:
            text+=input
    return {
        "text":text,
        "selifs":selifs,
        "blackets":blackets
    }

def export_to_json(filename:str,data)->None:
    contents=[]
    csv_result=[["id","text_id","header_type","content"]]
    row_id=1
    target_text_id=0
    text_id=0
    for t in data["contents"]:
        if t["header"]=="":continue
        text_inputs=[]
        texts=[]
        selifs=[]
        blackets=[]
        for i in split_texts(t["text"]):
            if i[-1]=="。" or i[-1]=="．":
                text_inputs.append(i)
                dat=text_to_data(text_inputs)# 文が終わったときにデータを整形し、 text_to_data を呼ぶ
                # textにtext_idを付与
                texts.append({
                    "text_id":text_id,
                    "text":dat["text"],
                })
                target_text_id=text_id
                csv_result.append([text_id,t["type"],t["header"],dat["text"]])
                text_id+=1
                # datのselifs, blacketsにtarget_text_idを付与。
                # selifs, blacketsにtext_idを付与。
                for selif in dat["selifs"]:
                    selif["target_text_id"]=target_text_id
                    selif["text_id"]=text_id
                    csv_result.append([text_id,t["type"],t["header"],selif["content"]])
                    text_id+=1
                selifs.extend(dat["selifs"])
                for blacket in dat["blackets"]:
                    blacket["target_text_id"]=target_text_id
                    blacket["text_id"]=text_id
                    csv_result.append([text_id,t["type"],t["header"],blacket["content"]])
                    text_id+=1
                blackets.extend(dat["blackets"])
                text_inputs=[]
            else:
                text_inputs.append(i) #文を蓄積する
        dat=text_to_data(text_inputs)# 文が終わったときにデータを整形し、 text_to_data を呼ぶ
        if dat["text"]!="":
            # textにtext_idを付与
            texts.append({
                "text_id":text_id,
                "text":dat["text"],
            })
            target_text_id=text_id
            csv_result.append([text_id,t["type"],t["header"],dat["text"]])
            text_id+=1
            # datのselifs, blacketsにtarget_text_idを付与。
            # selifs, blacketsにtext_idを付与。
            for selif in dat["selifs"]:
                selif["target_text_id"]=target_text_id
                selif["text_id"]=text_id
                csv_result.append([text_id,t["type"],t["header"],selif["content"]])
                text_id+=1
            selifs.extend(dat["selifs"])
            for blacket in dat["blackets"]:
                blacket["target_text_id"]=target_text_id
                blacket["text_id"]=text_id
                csv_result.append([text_id,t["type"],t["header"],blacket["content"]])
                text_id+=1
            blackets.extend(dat["blackets"])
        contents.append({
            "type":t["type"],
            "header":t["header"],
            #"header_text":t["header_text"],
            "texts":texts,
            "selifs":selifs,
            "blackets":blackets,
        })
    obj={
        "contents":contents
    }
    with open(filename+".json", 'w', encoding='utf8', newline='') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    import csv

    with open(filename+".csv", 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in csv_result:
            writer.writerow(row)
            
import glob
import os

def main():
    os.makedirs("06", exist_ok=True)
    files = glob.glob("./05/*.json")

    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        contents=json.load(contents)
        #print(contents)
        print(f"入力 {len(contents)}行")
        output_path=os.path.splitext(os.path.basename(file))[0]
        #print(f"出力 {len(container)}行")
        export_to_json(f"./06/{output_path}",contents)
        
if __name__=="__main__":
    main()