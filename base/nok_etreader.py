from csv import excel_tab
import lxml.etree as ET

class NokiaXML(object):
    def __init__(self):

        self.all_mo = dict()
        self.all_p = dict()

        self.set_class = set()
        self.set_p = set()

        self.getp = self.getdata_p
        self.startp = self.start_p

        self.this_list = ''

        self.mtype = ['raml']
        self.n = 0


    # DADOS DO PARAMETRO
    def getdata_p(self, d):
        self.this_mo[self.this_p] = d

    def getdada_p_list(self, d):
        if self.this_p in self.this_item:
            self.this_item[self.this_list] += '~' + d
        else:
            self.this_item[self.this_list] = d

    def getdada_p_item(self, d):
        if self.this_p in self.this_item:
            self.this_item[self.this_p] += '~' + d
        else:
            self.this_item[self.this_p] = d


    # INICIO DO PARAMETRO
    def start_p(self, n):
        self.this_p = n
        self.set_p.add(self.this_p)

    def start_p_list(self):
        self.this_p = self.this_list
        self.set_p.add(self.this_p)

    def start_p_item(self, n):
        self.this_p = self.this_list + '_' + n


    # LEITURA
    def start(self, tag, attrib):

        t = tag.split('}')[-1]
        match t:  # Na ordem do mais frequente

            case 'p':
                self.mtype.append('p')

                try:
                    self.startp(str(attrib['name']))
                except:
                    self.startp() # P sem LIST
                
            case 'list':
                self.mtype.append('list')
                self.startp = self.start_p_list
                self.getp = self.getdada_p_list

                self.this_item = dict()

                self.this_list = attrib.get('name')   #TODO Rever parametros de listas sem ITEM.

            case 'item':
                self.mtype.append('item')
                self.startp = self.start_p_item
                self.getp = self.getdada_p_item

            case 'managedObject':
                self.mtype.append('mo')

                self.mo_id = attrib['id']
                self.mo_class = attrib['class']
                self.mo_dn = attrib['distName']
                
                # Primeiro parâmetro
                self.this_mo = {'DN': self.mo_dn}
                self.set_p = {'DN'}

                sdn = self.mo_dn.split('/')
                for pdn in sdn[1:]:
                    cdn = pdn.split('-')
                    self.this_mo[cdn[0]] = cdn[1]
                    self.set_p.add(cdn[0])
                
                self.this_mo['ID'] = self.mo_id
                self.set_p.add('ID')

                if self.mo_class not in self.set_class:
                    self.all_mo[self.mo_class] = dict()
                    self.all_p[self.mo_class] = list()

                self.set_class.add(self.mo_class)
                

    def end(self, tag):
        
        t = tag.split('}')[-1]
        match t:  # Na ordem do mais frequente

            case 'p':
                self.mtype.pop()
                del self.this_p

            case 'list':
                self.mtype.pop()

                self.this_mo.update(self.this_item)
                del self.this_item

                self.getp = self.getdata_p
                self.startp = self.start_p
                self.this_list = ''

            case 'item':
                self.mtype.pop()
                self.getp = self.getdata_p

            case 'managedObject':
                self.mtype.pop()
                
                # Save this_mo in all_mo dictionary
                self.all_mo[self.mo_class][self.mo_id] = self.this_mo

                # Finds new parameters
                list_newp = list(self.this_mo.keys())
                full_plist = self.all_p[self.mo_class]

                if len(full_plist) >  0:
                    list_missing = list(self.set_p - set(full_plist))

                else:
                    list_missing = list_newp

                # Adds new parameters
                self.all_p[self.mo_class].extend(list_missing)

                self.n +=1
                self.mo_id = 0
                self.mo_class = ''
                self.mo_dn = ''
                self.set_p = set()
                del self.this_mo

    def data(self, data):
        if self.mtype[-1] == 'p':
            self.getp(data)

    def close(self):
        print("  + Done: %d elements found." % self.n)
        return self.all_mo, self.all_p


def process(xml_file, output_path, fReadType, opt_list):

    str_ignored = ''
    str_added = ''
    
    parser = ET.XMLParser(target = NokiaXML())
    results, params = ET.parse(xml_file, parser)

    print("\n# Exporting elements...")

    for m,d in results.items():

        if (fReadType != 'READALL') and (m not in opt_list):
            str_ignored += '\n    - ' + m.ljust(15) + str(len(d)).rjust(6) + ' elements, ' + str(len(params[m])).rjust(3) + ' params'
            continue

        str_added += '\n    - ' + m.ljust(15) + str(len(d)).rjust(6) + ' elements, ' + str(len(params[m])).rjust(3) + ' params'

        output_file = output_path + m + '.csv'
        out = open(output_file, 'w')

        pList = params[m]
        ibp = pList.index('ID') + 1

        bp = pList[:ibp] 
        pNames = pList[ibp:]
        pNames.sort()

        bp.extend(pNames)
        mycols = ';'.join(bp)

        out.write(mycols)
        out.write('\n')

        for id,p in d.items():
            
            myvals = ''
            for pp in bp:

                try:
                    myvals += ';' + p[pp]
                except:
                    myvals += ';'

            myvals = myvals[1:] + '\n'
            out.write(myvals)
                
        out.close()

    with open(output_path + "_resultado.txt", 'w') as f:            #, encoding = 'utf-8'
        f.write("Elements exported:\n")
        f.write(str_added)
        f.write("\n\nElements ignored:\n")
        f.write(str_ignored)

    print("\n  + Exported elements:\n" + str_added)
