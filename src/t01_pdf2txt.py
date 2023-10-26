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
from typing import List, Tuple, Dict, Set, Any
import sys

def get_objs(layout, results:List):
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
    import os
    result=[]
    if not os.path.isfile(path):
        print(f"{path} could not loaded")
        return None
    print(f"read {path}")

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
        for index, page in enumerate(PDFPage.create_pages(document)):
            interpreter.process_page(page)
            layout = device.get_result()
            results:list = []
            get_objs(layout, results)
            result_page={"page":index+1,"contents":results}
            result.append(result_page)
    return result

def main(path):
    data=pdf_to_cell(path)
    if data is None:
        print("file not found")
        return {
        "header":{
            "page_count":0
        },
        "pages":[]
    }
    print("phase 1 converted")
    return {
        "header":{
            "page_count":len(data)
        },
        "pages":data
    }

def export_to_json(filename:str,data)->None:
    import json
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

inputPath = sys.argv[1]
outputPath = sys.argv[2]

res=main(inputPath)
print("system completed")
export_to_json(outputPath,res)
