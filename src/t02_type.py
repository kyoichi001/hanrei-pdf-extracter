
from typing import List, Tuple, Dict, Set,Optional,Final,TypedDict
class Header(TypedDict):
    texts_count:int
class OutputData(TypedDict):
    header:Header
    contents:List[str]