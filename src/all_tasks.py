import t01_pdf2txt
import t02_justify_sentence
import t03_detect_header
import t04_split_section
import t05_detect_header_text
import t05_ignore_header_text
import t06_split_centence
import t07_filter_time
import t08_add_extention

print("=====================task 01=====================")
t01_pdf2txt.main("./pdf","./01")
print("=====================task 02=====================")
t02_justify_sentence.main("./01","./02")
print("=====================task 03=====================")
t03_detect_header.main("./02","./03")
print("=====================task 04=====================")
t04_split_section.main("./03","./04")
#print("=====================task 05=====================")
t05_detect_header_text.main("./04","./05")
#t05_ignore_header_text.main("./04","./05")
print("=====================task 06=====================")
t06_split_centence.main("./05","./06")
print("=====================task 07=====================")
t07_filter_time.main("./06","./07")
print("=====================task 08=====================")
t08_add_extention.main("./06","./08")

