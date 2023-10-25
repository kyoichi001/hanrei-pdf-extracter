import t01_pdf2txt
import t02_justify_sentence
import t03_detect_header
import t04_split_section
#import t05_detect_header_text
import t05_ignore_header_text
import t06_split_centence
#import t07_filter_time
import t08_add_extention
import sys

def export_to_json(filename:str,data)->None:
    import json
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

inputPath = sys.argv[1]
outputPath = sys.argv[2]

print("=====================task 01=====================")
res=t01_pdf2txt.main(inputPath)
print("=====================task 02=====================")
res=t02_justify_sentence.main(res)
print("=====================task 03=====================")
res=t03_detect_header.main(res)
print("=====================task 04=====================")
res=t04_split_section.main(res)
print("=====================task 05=====================")
#t05_detect_header_text.main("./04","./05")
res=t05_ignore_header_text.main(res)
print("=====================task 06=====================")
res=t06_split_centence.main(res)
#print("=====================task 07=====================")
#res=t07_filter_time.main(res)
print("=====================task 08=====================")
res=t08_add_extention.main(res)

export_to_json(outputPath,res)

print(f"exported to : {outputPath}")
