from typing import Any
import re

# function to extract urls from user's messages
def extract_urls(message: str) -> list[Any]:
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    urls = url_pattern.findall(message)
    return urls