import csv
from typing import List, Tuple, Dict, Set,Optional,TypedDict
import re
import json

class HanreiHeader(TypedDict):
    """
    箇条書きのタイプと内容のペア
    """
    header_type:str
    header:str
class HanreiSection(TypedDict):
    """
    箇条書きとその内容、その他付加情報
    """
    header:HanreiHeader
    text:str
    indent:int
    first_line:str
class HeaderRule:
    """
    箇条書きの判定ルール
    """
    def __init__(self,name:str,data:List[str],regexp:str,ignore_order:bool=False,ignore_letters:str="") -> None:
        self.name=name
        self.data=data
        self.regex=regexp
        self.ignore_order=ignore_order
        self.ignore_letters=ignore_letters
    def is_head(self,value:str)->bool:
        if self.data is None:return False
        return value==self.data[0]
    def is_valid(self,text:str)->bool:
        """
        header_type, headerがデータ内に存在するものかどうか
        """
        if self.data is None:return re.fullmatch(f"^{self.regex}",text) is not None#もし順番を定義するdataが存在しない場合、順番は考慮せず、正規表現にマッチするかのみ考慮
        return text in self.data
    def match(self,text:str)->bool:return re.fullmatch(f"^{self.regex}",text) is not None
    def get_index(self,text:str)->Optional[int]:
        if self.data is None:return None
        return self.data.index(text)


class HeaderChecker:
    """
    文章が箇条書きになりうるかどうか判定
    """
    def __init__(self,header_json) -> None:
        #箇条書き
        headers=header_json["rules"]
        self.rules=[HeaderRule(i["name"],i.get("data",None),i["regex"],i.get("order",False),i.get("ignore_letters","")) for i in headers]
    def match_header(self,txt:str)->bool:
        for i in self.rules:
            if i.match(txt):return True
        return False
    def is_collect(self,header_type:str,old_txt:str)->bool:
        rule=self.get_rule(header_type)
        if rule is None:
            print("error!")
            return False
        if rule.ignore_letters=="" or old_txt=="":return True
        #print(rule.ignore_letters)
        return old_txt[-1] not in rule.ignore_letters
        
    def get_header_type(self,txt:str)->Tuple[HanreiHeader,str]:
        for i in self.rules:
            r=re.match(f"^{i.regex}",txt)
            if r is not None:#マッチした箇条書きの種類を返す
                return {"header_type":i.name,"header":r.group()},txt[r.end():]
        return {"header_type":"unknown","header":""},txt #どの箇条書きにもマッチしない

    def is_head(self,header:str)->bool:
        for i in self.rules:
            if i.is_head(header):return True
        return False

    def is_valid(self,header:HanreiHeader)->bool:
        """
        header_type, headerがデータ内に存在するものか
        """
        rule=self.get_rule(header["header_type"])
        if rule is None:return False
        return rule.is_valid(header["header"])

    def get_index(self,header:HanreiHeader)->Optional[int]:
        """
        その箇条書きが何番目のものか
        """
        rule=self.get_rule(header["header_type"])
        if rule is None:return False
        return rule.get_index(header["header"])

    def get_rule(self,header_type:str)->Optional[HeaderRule]:
        for i in self.rules:
            if i.name==header_type:return i
        return None

class HeaderList:
    def __init__(self,checker:HeaderChecker) -> None:
        self.header_indexes:List[int]=[]
        self.headers:List[str]=[]
        self.header_types:List[str]=[]
        self.headerChecker=checker

    def current_indent(self)->int:return len(self.header_types)
    def current_headers(self)->str:return str(self.headers)

    #親以前に同じ種類の箇条書きがあるか
    def _has_before(self,header_type:str)->bool: return header_type in self.header_types
    #順番を無視していいタイプの箇条書きか
    def _ignore_order(self,header:HanreiHeader)->bool:return header["header_type"]=="others"

    #抽出された箇条書き候補が次の箇条書きとして正しいかどうか判定
    def is_next_header(self,header:HanreiHeader)->bool:
        if len(self.header_types)==0: return self.headerChecker.is_head(header["header"]) #headerが登録されていなかったら、headerが先頭のものかで返す
        if self.headerChecker.is_valid(header)==False:return False
        target_index=self.headerChecker.get_index(header)
        if self.header_types[-1]==header["header_type"]: #headerが直前のheaderと同じタイプだったら
            if self._ignore_order(header):return True
            return target_index==self.header_indexes[-1]+1 #headerが直前のheaderの次に位置するものか
        if self._has_before(header["header"]): #headerが以前に同じタイプが登録されてたら
            if self._ignore_order(header):return True
            index=self.header_types.index(header["header_type"])
            return target_index==self.header_indexes[index]+1 #headerが以前のheaderの次に位置するものか
        if self._ignore_order(header):return True
        return self.headerChecker.is_head(header["header"])#headerが以前と同じ種類になく、先頭のものだった場合

    def add_header(self,header:HanreiHeader)->None:
        if len(self.header_types)==0: #なにも登録されてなかったら
            self.header_types.append(header["header_type"])
            self.headers.append(header["header"])
            self.header_indexes.append(0)
            return 
        if self.header_types[-1]==header["header_type"]:#直前のタイプと同じだったら
            self.headers[-1]=header["header"]
            self.header_indexes[-1]+=1
            return
        if self._has_before(header["header_type"]):#以前にも同じタイプのヘッダーがあれば
            while self.header_types[-1]!=header["header_type"]:
                self.header_types.pop(-1)
                self.headers.pop(-1)
                self.header_indexes.pop(-1)
            self.headers[-1]=header["header"]
            self.header_indexes[-1]+=1
            return
        #まったく新しいタイプ
        self.header_types.append(header["header_type"])
        self.headers.append(header["header"])
        self.header_indexes.append(0)

    def reset(self)->None:#全箇条書き削除
        self.headers.clear()
        self.header_indexes.clear()
        self.header_types.clear()

def export_to_json(filename:str,data:List[HanreiSection])->None:
    contents=[]
    texts_count=0
    texts_len_max=0
    texts_len_avg=0
    for t in data:
        l=len(t["text"])
        texts_count+=1
        texts_len_max=max(texts_len_max,l)
        texts_len_avg+=l
        contents.append({
            "type":t["header"]["header_type"],
            "header":t["header"]["header"],
            "first_line":t["first_line"],
            "text":t["text"]
           # "indent":t.indent,
        })
    obj={
        "header":{
            "words_count":texts_len_avg,#文字数
            "texts_count":texts_count,
            "texts_len_max":texts_len_max,
            "texts_len_avg":texts_len_avg/texts_count,
        },
        "contents":contents
    }
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def main_func(contents,headerChecker:HeaderChecker)->List[HanreiSection]:
    text=""
    current_header:HanreiHeader={"header_type":"","header":""}
    headerList = HeaderList(headerChecker)
    container:List[HanreiSection]=[]
    main_section_headers=["判決","主文","事実及び理由"]
    first_line=""
    for content in contents:
        header=content["header"]
        t=content["texts"]
        indent=headerList.current_indent()
        if header in main_section_headers:# 主文、事実及び理由の場合
            container.append({"header":current_header,"text":text,"indent":indent,"first_line":first_line})
            headerList.reset()
            container.append({"header":{"header_type":"main_section","header":header},"text":"_","indent":0,"first_line":""})
            text=""
            first_line=""
            current_header={"header_type":"","header":""}
            continue
        if headerChecker.match_header(header):# 箇条書きなら改行
            #print(header)
            #print(text)
            txt_obj,txt=headerChecker.get_header_type(header)
            #抽出されたテキストが次の箇条書きでかつ、前の文を加味したとき正しいか
            flag1=headerList.is_next_header(txt_obj)
            flag2=headerChecker.is_collect(txt_obj["header_type"],text)
            #flag3=headerChecker.is_collect2(txt_obj.header,txt)
            if flag1 and flag2:
                container.append({"header":current_header,"text":text,"indent":indent,"first_line":first_line})
                #if txt_obj.header_type=="th_full_num" or txt_obj.header_type=="th_kanji_num":
                #    headerList.reset()#第nのとき、リセットする
                headerList.add_header(txt_obj)
                if len(t)==0: #もしそのヘッダー候補にテキストがなければ、次のヘッダー候補がヘッダーでないとき、その文がfirst_lineになる・・・
                    first_line=""
                    text=""
                else:
                    first_line=t[0]
                    text="".join(t[1:])
                current_header=txt_obj
            else:
                if first_line=="" and len(t)>0:
                    first_line=header+t[0]
                    text="".join(t[1:])
                else:
                    text+=header+"".join(t)
        else:
            if first_line=="" and len(t)>0:
                first_line=header+t[0]
                text="".join(t[1:])
            else:
                text+=header+"".join(t)
    container.append({"header":current_header,"text":text,"indent":headerList.current_indent(),"first_line":first_line})
    return container
            
import glob
import os

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    files = glob.glob(f"{inputDir}/*.json")

    header_file = open("./rules/headers.json", "r", encoding="utf-8")
    headers_obj=json.load(header_file)
    headerChecker=HeaderChecker(headers_obj)

    for file in files:
        print(file)
        contents = open(file, "r", encoding="utf-8")
        data:list=json.load(contents)["contents"]
        print(f"入力 {len(data)}行")
        container=main_func(data,headerChecker)
        output_path=os.path.splitext(os.path.basename(file))[0]
        print(f"出力 {len(container)}行")
        export_to_json(f"{outputDir}/{output_path}.json",container)

if __name__=="__main__":
    main("./03","./04")