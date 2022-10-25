# https://qiita.com/mima_ita/items/d99afc28b6f51479f850

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (
    LAParams,
    LTContainer,
    LTTextLine,
)
from typing import List, Tuple, Dict, Set

import sys

def get_objs(layout, results):
    if not isinstance(layout, LTContainer):
        return
    for obj in layout:
        if isinstance(obj, LTTextLine):
            results.append({
                 'text' : obj.get_text(),
                 "x":obj.bbox[0],
                 "y":obj.bbox[1],
                 })
        get_objs(obj, results)

def pdf_to_cell(path:str):
    result=[]
    with open(path, "rb") as f:
        parser = PDFParser(f)
        document = PDFDocument(parser)
        if not document.is_extractable: raise PDFTextExtractionNotAllowed
        # https://pdfminersix.readthedocs.io/en/latest/api/composable.html#
        laparams = LAParams(
            all_texts=True,
        )
        rsrcmgr = PDFResourceManager()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        p_count=0
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            results = []
            get_objs(layout, results)
            result_page={"page":p_count+1,"contents":results}
            p_count+=1
            result.append(result_page)
    return result

def export_to_json(filename:str,data)->None:
    obj={
        "header":{
            "page_count":len(data)
        },
        "pages":data
    }
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

import glob
import os
import json

def main():
    args = sys.argv

    os.makedirs("01", exist_ok=True)

    if len(args)==1:
        files = glob.glob("./pdf/*.pdf")
        for file in files:
            print(file)
            output_path=os.path.splitext(os.path.basename(file))[0]
            export_to_json(f"./01/{output_path}.json",pdf_to_cell(file))
    else:
        print(args[1])
        #for i in pdf_to_cell(args[1]):
        #    print(i)

if __name__=="__main__":
    main()