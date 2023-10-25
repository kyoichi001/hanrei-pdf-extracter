
from typing import List, Tuple, Dict, Set,Optional,Final,TypedDict

class Header(TypedDict):
    page_count:int
class PageContent(TypedDict):
    text:str
    x:float
    y:float
class Page(TypedDict):
    page:int
    contents:List[PageContent]
class OutputData(TypedDict):
    header:Header
    pages:List[Page]