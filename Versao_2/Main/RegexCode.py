import re
regexPreco = r'R\$((?:\d{1,3}\.)*\d{1,3}),\d{2}'


def RePreco(preco) :
    newPreco =  re.search(regexPreco, preco).group(1)
    try :    return newPreco.replace('.', '')
    except : return newPreco







