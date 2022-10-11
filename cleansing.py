import re
from unidecode import unidecode
import string

#replace ascii
def replace_ascii(text):
    #text = text.encode().decode('unicode_escape')
    #text = bytes(text, 'latin').decode('utf-8') 
    return re.sub(r"\\x[A-Za-z0-9./]+", "",unidecode(text))


def remove_special_char(text):
    # remove tab, new line, ans back slice
    text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
    # remove non ASCII (emoticon, chinese word, .etc)
    text = text.encode('ascii', 'replace').decode('ascii')
    # remove mention, link, hashtag
    text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())
    # remove incomplete URL
    return text.replace("http://", " ").replace("https://", " ")
                

#remove number
def remove_number(text):
    return  re.sub(r"\d+", "", text)


#remove punctuation
def remove_punctuation(text):
    return text.translate(str.maketrans("","",string.punctuation))


#remove whitespace leading & trailing
def remove_whitespace_LT(text):
    return text.strip()


#remove multiple whitespace into single whitespace
def remove_whitespace_multiple(text):
    return re.sub('\s+',' ',text)

# remove single char
def remove_single_char(text):
    return re.sub(r"\b[a-zA-Z]\b", "", text)

#hapus url
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)
