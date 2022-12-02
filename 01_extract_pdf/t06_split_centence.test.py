
import t06_split_centence
texts=[
    "「XXX X)XXXX。」XXX",
    "「XXXX」XXX(XXXX)",
    "(XXX(XXX)XXX)(XXX)",
    "(((XXX))XXX)(XXX)",
    "(XXX(「XXX」XXX))",
    "「XXX(「XXX」XXX)」(XXX)XXXXXX「XXX」",
    "XXX(XXXX)「XXXX X) X)XX。」XXX X)XXX X)XXX。XXX。XX。",
    "XXX(XXXX)「XXXX X) XX。」XXX X XXX XXX。)XXX。XX。",
    "XX)XX",
    "XX(XX",
    "XXXX"
]

for text in texts:
    print("======================")
    a=t06_split_centence.extract_kakko(text)
    print(text," : ",a)