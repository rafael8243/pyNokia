from csv import excel_tab
import lxml.etree as ET
from numpy import concatenate

class NokiaXML(object):
    def __init__(self):

        print('Parsing ...')

        self.set_class = set()        
        self.all_mo = dict()

        self.all_p = dict()
        self.set_p = set()

        self.mtype = ['raml']
        self.this_list = ''
        self.isItem = False
        self.n = 0

    def start(self, tag, attrib):

        t = tag.split('}')[-1]
        match t:  # Na ordem do mais frequente

            case 'p':
                self.mtype.append('p')
                self.this_p = self.this_list + str(attrib.get('name'))
                self.set_p.add(self.this_p)
                
            case 'list':
                self.mtype.append('list')
                self.this_list = attrib.get('name') + '_'

            case 'item':
                self.mtype.append('item')
                self.isItem = True

            case 'managedObject':
                self.mtype.append('mo')

                self.mo_id = int(attrib['id'])
                self.mo_class = attrib['class']
                self.mo_dn = attrib['distName']

                self.this_mo = dict()   #inicia novo elemento
                #self.this_mo['DN'] = self.mo_dn

                if self.mo_class not in self.set_class:
                    self.all_mo[self.mo_class] = dict()
                    self.all_p[self.mo_class] = list()

                self.set_class.add(self.mo_class)

                #print("id:",self.mo_id)
                

    def end(self, tag):
        
        t = tag.split('}')[-1]
        match t:  # Na ordem do mais frequente

            case 'p':
                self.mtype.pop()
                del self.this_p

            case 'list':
                self.mtype.pop()
                self.this_list = ''

            case 'item':
                self.mtype.pop()
                self.isItem = False

            case 'managedObject':
                self.mtype.pop()
                
                self.all_mo[self.mo_class][self.mo_id] = self.this_mo

                list_newp = list(self.this_mo.keys())
                full_plist = self.all_p[self.mo_class]

                if len(full_plist) >  0:
                    list_missing = list(set(list_newp) - self.set_p)
                    #list_newp.extend(list_missing)
                else:
                    list_missing = list_newp                

                self.all_p[self.mo_class].extend(list_missing)

                self.n +=1
                self.mo_id = 0
                self.mo_class = ''
                self.mo_dn = ''
                del self.this_mo


    def data(self, data):
        if self.mtype[-1] == 'p':
            self.this_mo[self.this_p] = data

    def close(self):
        #nLNBTS = len(self.all_mo.get('LNBTS'))
        #nBCF = len(self.all_mo.get('BCF'))
        print("\nParsing done! \n - Found %d Elements.\n" % self.n)
        return self.all_mo, self.all_p

def process(xml_file, caminho):

    #ttt = ET.parse(xml_file)
    #root = ttt.getroot()
    #root.tag
    
    parser = ET.XMLParser(target = NokiaXML())
    results, params = ET.parse(xml_file, parser)

    for m,d in results.items():

        outfile = caminho + m + '.csv'
        out = open(outfile, 'w')

        bp = params[m]

        mycols = ','.join(bp)
        out.write(mycols)
        out.write('\n')

        #print('Exporting %s...' % m)
        for id,p in d.items():
            
            myvals = ''

            for pp in bp:

                try:
                    myvals += ',' + p[pp]
                except:
                    myvals += ','

            myvals = myvals[1:] + '\n'

            out.write(myvals)
        
        out.close()

 