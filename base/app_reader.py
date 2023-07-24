import os

from threading import Thread
from time import perf_counter, localtime, strftime
from base import nok_etreader as nokr

class nokia_parser:
    def __init__(self):
        
        self.board_size = '650x360'

        self.base_path = os.path.expanduser('~/Documents')

        self.xml_files_path = "C:/C/DUMP/NOK/2G_NOK5-20230306.xml"                
        self.xml_files_info = []
        
        self.READ_TYPE = "DEFAULT"

    
    def check_file(self, input_files) -> bool:

        for i in range(len(input_files)):
            path_split = os.path.split(input_files[i])

            if os.path.exists(input_files[i]):
                self.base_path = os.chdir(path_split[0]) # Change base directory to last used
                self.xml_files_path = input_files #save file paths

                xml_size = round(os.stat(self.xml_files_path[i]).st_size / (1024 * 1024),2)
                self.xml_files_info.append(f'Found {path_split[1]} ({xml_size} MB)')

                return True

            else:
                self.xml_files_info.append(f'Not Found {path_split[1]}')
                return False


    def threading_read(self):
        # Call work function
        t1=Thread(target=self.read_file)
        t1.start()


    def read_file(self):

        tm_start = perf_counter()

        default_list = ['LNCEL_FDD', 'LNBTS', 'LNCEL', 'IRFIM', 'SIB', 'LNMME','MOPR',
                        'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'LNBTS_FDD', 'WNCELG', 'WNBTS',
                        'ADJI', 'WBTS', 'ADJS', 'ADJD', 'WCEL', 'FMCS', 'HOPS', 
                        'COCO', 'ADJG', 'ADJL', 'RNC', 'LAPD', 'MAL', 'TRX', 
                        'BCF', 'DAP', 'BTS', 'ADCE', 'ADJW', 'BAL', 'BSC']

        mtime = localtime(os.path.getmtime(self.xml_files_path[0])) #TODO CONTINUAR
        timestamp = strftime('%Y%m%d', mtime)

        caminho = os.path.dirname(self.xml_files_path[0]) + "/output/"
        output = os.path.splitext(self.xml_files_path[0])[0] + ".xlsx"

        # Limpa parta temporária de saída
        old_files = os.listdir(caminho)

        for f in old_files:
            if f.endswith(".csv"):
                os.remove(os.path.join(caminho, f))

        # Build Output Filename
        i = 0
        while os.path.exists(output):
            i = i + 1
            output = os.path.splitext(self.xml_files_path[0])[0] + " (" + str(i) + ").xlsx"

        # Read and export selected elements 
        nokr.process(self.xml_files_path, caminho, self.fread_type, default_list)

        tm_parse = perf_counter()
        self.print_box('\n# Merging data...')

        MergeCSV(caminho, output, self.root)

        tm_merge = perf_counter()
        te_parse = round(tm_parse - tm_start , 2)
        te_merge = round(tm_merge - tm_parse , 2)

        self.print_box(f'\n\n  Read : {te_parse:7.2f} s\n')
        self.print_box(f'  Merge: {te_merge:7.2f} s\n')

        te_all = round(tm_merge - tm_start , 2)
        self.print_box(f'         ----------\n  Total: {te_all:7.2f} s')

        self.print_box("\n\n# Finished!\n  = " + output)