import glob
import os
import csv
from typing import List, Tuple, Dict, Set, Optional,Final,Union,Any
import re
import json
import re

def extract_kakko(text: str) -> List[str]:
    """
    カッコの入っている文からカッコとそれ以外を抽出
    """
    def is_all_zero(table, ignore_key) -> bool:
        for key in table:
            if (ignore_key is None or key != ignore_key) and table[key] != 0:
                return False
        return True

    res_wokakko = ""
    res_kakko = ""
    pair_kakko:Final = {"(": ")", ")": "(", "「": "」", "」": "「"}
    kakko_count = {"(": 0, "「": 0}
    target_kakko = ""
    res = []
    if text == "":
        return [""]
    if text[0] == "(" or text[0] == "「":
        target_kakko = text[0]
        kakko_count[text[0]] += 1
    if kakko_count["("] >= 1 or kakko_count["「"] >= 1:
        res_kakko += text[0]
    else:
        res_wokakko += text[0]
    for i in range(1, len(text)):
        if text[i] == ")" or text[i] == "」":
            kakko_count[pair_kakko[text[i]]] -= 1
            if kakko_count[pair_kakko[text[i]]] == 0 and pair_kakko[text[i]] == target_kakko:
                res.append(res_kakko+text[i])
                res_kakko = ""
                kakko_count = {"(": 0, "「": 0}
                target_kakko = ""
                continue
        if text[i] == "(" or text[i] == "「":
            kakko_count[text[i]] += 1
            if is_all_zero(kakko_count, text[i]):
                target_kakko = text[i]
                res.append(res_wokakko)
                res_wokakko = ""
        if target_kakko != "":
            res_kakko += text[i]
        else:
            res_wokakko += text[i]
    if target_kakko != "":
        res.append(res_kakko)
    else:
        res.append(res_wokakko)
    return [i for i in res if i != ""]

def split_texts(text: str) -> List[str]:
    def split_text(text: str) -> List[str]:
        a = re.sub("。([^」\\)〕])", "。$\\1", text)
        texts_dat = a.split("$")
        if len(texts_dat) == 0:
            return [text]
        return texts_dat

    texts = extract_kakko(text)  # 文からカッコとそうでないのを区切る。配列を返す
    texts2: List[str] = []
    for txt in texts:
        if txt == "":
            continue
        if txt[0] == "(" or txt[0] == "「":  # そのテキストが「」・（）の形式の文だったら、「。」で区切らない
            texts2.append(txt)
            continue
        for i in split_text(txt):  # 「。」で区切る
            if i == "":
                continue
            texts2.append(i)
    return texts2

def text_to_data(inputs: List[str]):
    """
    一文からselifsやblacketsなどのデータを返す
    """
    selifs = []
    blackets = []
    text = ""
    raw_text=""
    current_selif_count = 0
    for input in inputs:
        if input[0] == "「":
            selifs.append({
                "target_selif": current_selif_count,  # その文の何番目の「セリフ」を置換するか
                "content": input
            })
            current_selif_count += 1
            text += "「セリフ」"
        elif input[0] == "(" or input[0] == "（":
            blackets.append({
                "position": len(text),  # 何文字目の前に埋め込むか（0なら最初の文字の前に埋め込む）
                "content": input,
            })
        else:
            text += input
        raw_text+=input
    return {
        "text": text,
        "selifs": selifs,
        "blackets": blackets,
        "raw_text":raw_text,
    }

def export_to_csv(filename: str, data) -> None:
    fact_reason=data["contents"]["fact_reason"]
    csv_result:list[list[Union[int,str]]] = [["id", "header", "header_text", "content"]]
    csv_raw_result:list[list[Union[int,str]]] = [["id", "header", "header_text", "content"]]
    text_id = 0
    raw_text_id=0
    for t in fact_reason["sections"]:
        if t["header"] == "":
            continue
        if t["text"]=="":
            csv_result.append([text_id, t["header"],t["header_text"] ,""])
            csv_raw_result.append([raw_text_id, t["header"],t["header_text"] ,""])
            raw_text_id+=1
            text_id+=1
        text_inputs = []
        for i in split_texts(t["text"]):
            if i[-1] == "。" or i[-1] == "．":
                text_inputs.append(i)
                # 文が終わったときにデータを整形し、 text_to_data を呼ぶ
                dat = text_to_data(text_inputs)
                csv_result.append([text_id, t["header"],t["header_text"] ,dat["text"]])
                csv_raw_result.append([raw_text_id, t["header"],t["header_text"] ,dat["raw_text"]])
                text_id += 1
                # datのselifs, blacketsにtarget_text_idを付与。
                # selifs, blacketsにtext_idを付与。
                for selif in dat["selifs"]:
                    csv_result.append([text_id, t["header"],t["header_text"] , selif["content"]])
                    text_id += 1
                for blacket in dat["blackets"]:
                    csv_result.append([text_id, t["header"],t["header_text"] , blacket["content"]])
                    text_id += 1
                text_inputs = []
                raw_text_id+=1
            else:
                text_inputs.append(i)  # 文を蓄積する
        dat = text_to_data(text_inputs)  # 文が終わったときにデータを整形し、 text_to_data を呼ぶ
        if dat["text"] != "":
            csv_result.append([text_id, t["header"],t["header_text"] , dat["text"]])
            csv_raw_result.append([raw_text_id, t["header"],t["header_text"] , dat["raw_text"]])
            text_id += 1
            # datのselifs, blacketsにtarget_text_idを付与。
            # selifs, blacketsにtext_idを付与。
            for selif in dat["selifs"]:
                csv_result.append(
                    [text_id, t["header"],t["header_text"] ,selif["content"]])
                text_id += 1
            for blacket in dat["blackets"]:
                csv_result.append(
                    [text_id, t["header"],t["header_text"] , blacket["content"]])
                text_id += 1
            raw_text_id+=1
    import csv

    with open(filename+".csv", 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in csv_result:
            writer.writerow(row)
    with open(filename+"_raw.csv", 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in csv_raw_result:
            writer.writerow(row)

def export_to_json(filename: str, data) -> None:
    res:Any={
        "signature":data["contents"]["signature"],
        "judgement":data["contents"]["judgement"],
        "main_text":{},
        "fact_reason":{},
    }
    main_text=data["contents"]["main_text"]
    fact_reason=data["contents"]["fact_reason"]
    contents = []
    target_text_id = 0
    text_id = 0
    for t in main_text["sections"]:
        text_inputs = []
        texts = []
        selifs = []
        blackets = []
        for i in split_texts(t["text"]):
            if i[-1] == "。" or i[-1] == "．":
                text_inputs.append(i)
                # 文が終わったときにデータを整形し、 text_to_data を呼ぶ
                dat = text_to_data(text_inputs)
                # textにtext_idを付与
                texts.append({
                    "text_id": text_id,
                    "text": dat["text"],
                    "raw_text":"".join(text_inputs)
                })
                target_text_id = text_id
                text_id += 1
                # datのselifs, blacketsにtarget_text_idを付与。
                # selifs, blacketsにtext_idを付与。
                for selif in dat["selifs"]:
                    selif["target_text_id"] = target_text_id
                    selif["text_id"] = text_id
                    text_id += 1
                selifs.extend(dat["selifs"])
                for blacket in dat["blackets"]:
                    blacket["target_text_id"] = target_text_id
                    blacket["text_id"] = text_id
                    text_id += 1
                blackets.extend(dat["blackets"])
                text_inputs = []
            else:
                text_inputs.append(i)  # 文を蓄積する
        dat = text_to_data(text_inputs)  # 文が終わったときにデータを整形し、 text_to_data を呼ぶ
        if dat["text"] != "":
            # textにtext_idを付与
            texts.append({
                "text_id": text_id,
                "text": dat["text"],
                "raw_text":"".join(text_inputs)
            })
            target_text_id = text_id
            text_id += 1
            # datのselifs, blacketsにtarget_text_idを付与。
            # selifs, blacketsにtext_idを付与。
            for selif in dat["selifs"]:
                selif["target_text_id"] = target_text_id
                selif["text_id"] = text_id
                text_id += 1
            selifs.extend(dat["selifs"])
            for blacket in dat["blackets"]:
                blacket["target_text_id"] = target_text_id
                blacket["text_id"] = text_id
                text_id += 1
            blackets.extend(dat["blackets"])
        app_obj = {
            "type": t["type"],
            "header": t["header"],
            "indent":t["indent"]
        }
        if len(texts) != 0: app_obj["texts"] = texts
        if len(selifs) != 0: app_obj["selifs"] = selifs
        if len(blackets) != 0: app_obj["blackets"] = blackets
        contents.append(app_obj)
    res["main_text"]={
        "header_text":data["contents"]["main_text"]["header_text"],
        "sections":contents
    }
    contents=[]
    for t in fact_reason["sections"]:
        text_inputs = []
        texts = []
        selifs = []
        blackets = []
        for i in split_texts(t["text"]):
            if i[-1] == "。" or i[-1] == "．":
                text_inputs.append(i)
                # 文が終わったときにデータを整形し、 text_to_data を呼ぶ
                dat = text_to_data(text_inputs)
                # textにtext_idを付与
                texts.append({
                    "text_id": text_id,
                    "text": dat["text"],
                    "raw_text":"".join(text_inputs)
                })
                target_text_id = text_id
                text_id += 1
                # datのselifs, blacketsにtarget_text_idを付与。
                # selifs, blacketsにtext_idを付与。
                for selif in dat["selifs"]:
                    selif["target_text_id"] = target_text_id
                    selif["text_id"] = text_id
                    text_id += 1
                selifs.extend(dat["selifs"])
                for blacket in dat["blackets"]:
                    blacket["target_text_id"] = target_text_id
                    blacket["text_id"] = text_id
                    text_id += 1
                blackets.extend(dat["blackets"])
                text_inputs = []
            else:
                text_inputs.append(i)  # 文を蓄積する
        dat = text_to_data(text_inputs)  # 文が終わったときにデータを整形し、 text_to_data を呼ぶ
        if dat["text"] != "":
            # textにtext_idを付与
            texts.append({
                "text_id": text_id,
                "text": dat["text"],
                "raw_text":"".join(text_inputs)
            })
            target_text_id = text_id
            text_id += 1
            # datのselifs, blacketsにtarget_text_idを付与。
            # selifs, blacketsにtext_idを付与。
            for selif in dat["selifs"]:
                selif["target_text_id"] = target_text_id
                selif["text_id"] = text_id
                text_id += 1
            selifs.extend(dat["selifs"])
            for blacket in dat["blackets"]:
                blacket["target_text_id"] = target_text_id
                blacket["text_id"] = text_id
                text_id += 1
            blackets.extend(dat["blackets"])
        app_obj = {
            "type": t["type"],
            "header": t["header"],
            "header_text":t["header_text"],
            "indent":t["indent"]
        }
        if len(texts) != 0:app_obj["texts"] = texts
        if len(selifs) != 0:app_obj["selifs"] = selifs
        if len(blackets) != 0:app_obj["blackets"] = blackets
        contents.append(app_obj)
    res["fact_reason"]={
        "header_text":data["contents"]["fact_reason"]["header_text"],
        "sections":contents
    }
    with open(filename+".json", 'w', encoding='utf8', newline='') as f:
        json.dump({"contents":res}, f, ensure_ascii=False, indent=2)

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
        export_to_json(f"{outputDir}/{output_path}", contents)
        export_to_csv(f"{outputDir}/{output_path}", contents)


if __name__ == "__main__":
    main("./05", "./06")
