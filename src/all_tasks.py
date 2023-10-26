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

#print("=====================task 01=====================", file=sys.stderr)
print(1,7)
res=t01_pdf2txt.main(inputPath)
#print("=====================task 02=====================", file=sys.stderr)
print(2,7)
res=t02_justify_sentence.main(res)
#print("=====================task 03=====================", file=sys.stderr)
print(3,7)
res=t03_detect_header.main(res)
#print("=====================task 04=====================", file=sys.stderr)
print(4,7)
res=t04_split_section.main(res)
#print("=====================task 05=====================", file=sys.stderr)
print(5,7)
#t05_detect_header_text.main("./04","./05")
res=t05_ignore_header_text.main(res)
#print("=====================task 06=====================", file=sys.stderr)
print(6,7)
res=t06_split_centence.main(res)
#print("=====================task 07=====================", file=sys.stderr)
#res=t07_filter_time.main(res)
#print("=====================task 08=====================", file=sys.stderr)
print(7,7)
res=t08_add_extention.main(res)
export_to_json(outputPath,res)

#print(f"exported to : {outputPath}", file=sys.stderr)
