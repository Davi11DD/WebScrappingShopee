import re

preco_re = r'R\$(?:(\d{1,3})\.)*(\d{1,3}),\d{2}'
def RePreco(preco) :
    newPreco =  re.search(preco_re, preco)
    ultPreco = f'{newPreco.group(1)}{newPreco.group(2)}'
    if 'none' in ultPreco :
        ultPreco.replace('None', '')
    return ultPreco









