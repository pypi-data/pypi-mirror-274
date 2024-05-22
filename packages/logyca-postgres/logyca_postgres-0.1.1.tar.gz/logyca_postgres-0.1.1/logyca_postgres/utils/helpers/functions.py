import urllib.parse

def html_escaping_special_characters(word:str)->str:
    '''Description
    :return str: For example, if you enter "kx@jj5/g", it returns "kx%40jj5%2Fg"
    '''
    return urllib.parse.quote_plus(word)