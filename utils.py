import re

def extract_name(text):
    """Extracts name from text."""
   
    regex = r'(?<=Имя: ).*'
    name = re.search(regex, text).group()

    return name