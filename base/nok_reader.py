import re
from select import select
from matplotlib.transforms import offset_copy
import numpy as np

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

def check_type(s):
    
    x = isParam(s)
    x = x if x else isList(s)
    x = x if x else isItem(s)
    x = x if x else isEndlist(s)
    x = x if x else isEnditem(s)
    x = x if x else isMO(s)    
    x = x if x else isEndMO(s)
    x = x if x else isListparam(s)    
    return x if x else 0


class OpenFile:

    def getNext(self):
        self.this_row = self.next_row
        self.next_row = self.file.readlines()


    def __init__(self, file_path):
        self.path = file_path
        self.file = open(file_path,'r')

        self.this_row = self.file.readlines()
        self.next_row = self.file.readlines()
    

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

def getP(f,s,p):
    try:
        r = re.search('="(.*)">(.*)<\/', s)
        n = r.group(1)
        v = r.group(2)
        
        p[n] = v    #Save Parameter Name & Value at param_dict

        return n
        #print(o, p, v)
    except:
        print("Param error:", s)

def getList(s):
    a=1

def getItem(s):
    a = s.split(' ')
    b=1

def closeList():
    a=1

def closeItem():
    a=1

# ============= PROCESSAR LINHA =============

def process(xml_file):

    oFile = OpenFile(xml_file)    

    while oFile.next_row != '':
        
        oFile.getNext()

        esse = check_type(oFile.this_row)
    
        match esse:
            case 0:
                pass

            case 'Param':
                nome = getP(file, next_row)
                return this_mo
            
            case 'MO':
                dn_dict = dict()
                this_mo = getMO(next_row, mo_set, dn_dict)
                
                param_dict[this_mo] = dn_dict   # Save DN columns in parameters
                
                #TODO está salvando por cima

                return this_mo

            case 'List Param':
                nome = getP(next_row)
                return this_mo

            case 'MO End':
                closeMO(this_mo, param_dict[this_mo])
                return None

            case 'List':
                nome = getList(next_row)
                inList = True
                return this_mo
            
            case 'List OFF':
                closeList()
                inList = False
                return this_mo
            
            case 'Item':
                nome = getItem(next_row)
                inItem = True
                return this_mo
            
            case 'Item OFF':
                closeItem()
                inItem = False
                return this_mo
    