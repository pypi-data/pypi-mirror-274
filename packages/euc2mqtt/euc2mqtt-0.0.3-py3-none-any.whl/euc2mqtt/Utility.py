import re

def id_format(s) -> str:
    return re.sub(r'[^a-zA-Z0-9\-\_]', '', re.sub(r'[\.\s]', '_', s))