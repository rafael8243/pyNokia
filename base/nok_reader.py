from pickle import FALSE, TRUE
import re
from select import select
import numpy as np

# ============= VERIFICAÇÕES PARA CADA TIPO DE LINHA =============

def isParam(s):
    o = ('<p name') in (' ' + s + ' ')
    a = [0,'Param'][o]
    return a

def isMO(s):
    o = ('<managedObject') in (' ' + s + ' ')
    a = [0,'MO'][o]
    return a

def isEndMO(s):
    o = ('</managedObject>') in (' ' + s + ' ')
    a = [0,'MO End'][o]
    return a

def isList(s):
    o = ('<list') in (' ' + s + ' ')
    a = [0,'List'][o]
    return a

def isListparam(s):
    o = ('<p>') in (' ' + s + ' ')
    a = [0,'List Param'][o]
    return a

def isItem(s):
    o = ('<item') in (' ' + s + ' ')
    a = [0,'Item'][o]
    return a

def isEndlist(s):
    o = ('</list') in (' ' + s + ' ')
    a = [0,'List OFF'][o]
    return a

def isEnditem(s):
    o = ('</item') in (' ' + s + ' ')
    a = [0,'Item OFF'][o]
    return a

# ============= LEITURA DAS LINHAS =============

def getMO(s,m,d):
    r = re.search(r'class=\"(\w*)\".+Name=\"(.+)\"\s', s)
    try:
        n = r.group(1)  # MO name
        p = r.group(2)  # MO path (distname)
        
        #k = re.findall(r'\/(\w+)-(\d+)?(?=\/|$)', d)        
        for k in re.finditer(r'\/(\w+)-(\d+)?(?=\/|$)', p):
            d[k.group(1)] = k.group(2)   # Elementos do DN

        m.add(n)    # Save MO Name at MO List

        return n
            
    except AttributeError:
        print(" * Erro no MO")
        c=0

def closeMO(n,p):
    a=1

def getP(s,p):
    try:
        r = re.search('="(.*)">(.*)<\/', s)
        n = r.group(1)
        v = r.group(2)
        
        p[n] = v    #Save Parameter Name & Value at param_dict

        return n
        #print(o, p, v)
    except:
        print("param error:", s)

def getList(s):
    a=1

def getItem(s):
    a = s.split(' ')
    b=1

def closeList():
    a=1

def closeItem():
    a=1

# ============= VERIFICAÇÕES DO TIPO DE LINHA =============

def check_type(s):
    
    x = isParam(s)
    x = x if x else isMO(s)
    x = x if x else isList(s)
    x = x if x else isListparam(s)
    x = x if x else isEndMO(s)
    x = x if x else isItem(s)
    x = x if x else isEndlist(s)
    x = x if x else isEnditem(s)
    return x if x else 0

# ============= PROCESSAR LINHA =============

def process(linha, mo_set, param_dict, this_mo):
    
    esse = check_type(linha)

    linha = linha.strip()
    
    match esse:
        case 0:
            return this_mo

        case 'Param':
            nome = getP(linha, param_dict[this_mo])
            return this_mo
        
        case 'MO':
            dn_dict = dict()
            this_mo = getMO(linha, mo_set, dn_dict)
            
            param_dict[this_mo] = dn_dict   # Save DN columns in parameters
            
            #TODO está salvando por cima

            return this_mo

        case 'List Param':
            nome = getP(linha)
            return this_mo

        case 'MO End':
            closeMO(this_mo, param_dict[this_mo])
            return None

        case 'List':
            nome = getList(linha)
            inList = TRUE
            return this_mo
        
        case 'List OFF':
            closeList()
            inList = FALSE
            return this_mo
        
        case 'Item':
            nome = getItem(linha)
            inItem = TRUE
            return this_mo
        
        case 'Item OFF':
            closeItem()
            inItem = FALSE
            return this_mo
    