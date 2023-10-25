
from typing import List, Tuple, Dict, Set,Optional,Final,TypedDict
class Section(TypedDict):
    header:str
    texts:list[str]
class Chapter(TypedDict):
    header_text:str
    sections:list[Section]
class Hanrei(TypedDict):
    signature:Chapter
    judgement:Chapter
    main_text:Chapter
    fact_reason:Chapter