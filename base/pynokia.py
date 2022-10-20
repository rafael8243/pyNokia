import os
import sys
import pandas as pd
from time import perf_counter, localtime, strftime

import nok_etreader as nokr


def AboutMe():
    return('''     
  =========================================================================
    PYNOKIA
  =========================================================================

    Este aplicativo converte exports XML da NOKIA em planilhas Excel.

    Sintaxe:

        pynokia [opção] <nome_do_arquivo>
    
    Opção: 
        
        -f\tConverte principais elementos do DUMP (padrão).
        -a\tConverte todos os elementos do DUMP.
        -l\tLista os principais elementos.
    
    Desenvolvido por Rafael Bastos
     - Twitter: @rafael8243

  =========================================================================
    ''')

def MergeCSV(origem, destino):

    #csv_list = [origem + f for f in os.listdir(origem)]
    
    files = os.listdir(origem)
    csv_list = [origem + i for i in files if i.endswith('.csv')]

    print(f"  + Found {len(csv_list)} element types:")

    writer = pd.ExcelWriter(destino) # Arbitrary output name

    for csvfilename in csv_list:

        df = pd.read_csv(csvfilename)
        sname = csvfilename.split('\\')[-1].split('.')[0]
        print(f'    - {sname}')
        
        df.to_excel(writer, sheet_name=sname, index = False)
    
    print("\n# Saving output file...\n")
    writer.save()


if __name__ == '__main__':

    READ_TYPE = ''
    tm_start = perf_counter()

    default_list = ['LNCEL_FDD', 'LNBTS', 'LNADJ', 'LNCEL', 'IRFIM', 'SIB', 'LNADJL', 
    'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'LNBTS_FDD', 'ADJI', 'WBTS', 'ADJS', 
    'ADJD', 'WCEL', 'FMCS', 'HOPS', 'COCO', 'ADJG', 'ADJL', 'RNC', 'LAPD', 
    'MAL', 'TRX', 'BCF', 'ADJL', 'DAP', 'BTS', 'CSDAP', 'ADCE', 'ADJW', 'BAL',
    'BSC', 'LNMME','MOPR']

    # Get XML Filename
    #xml_file = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\dump_sample.xml"
    xml_file = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\Dump_20221020_3G_RBA.xml"
    
    if len(sys.argv) == 2: 
        xml_file = sys.argv[1]   #get file from command line
        READ_TYPE = 'READALL'

    if len(sys.argv) == 3: 
        xml_file = sys.argv[2]   #get file from command line

        txt_help = AboutMe()

        match sys.argv[1]:
            case "-a":
                print("Export All Elements.")
                READ_TYPE = 'READALL'

            case "-f":
                print("Export Default Elements.")
                READ_TYPE = 'DEFAULT'

            case "-l":
                print("Default Elements Listing:")
                print(default_list)
                quit()

            case _:
                print(txt_help)
                quit()

    # Check XML File
    if os.path.exists(xml_file):
        xml_size = round(os.stat(xml_file).st_size / (1024 * 1024),2)
        print(f'\n# Source file:\n\n  + {xml_file} ({xml_size} MB)')

    else:
        print(f'### ERROR: File does not exist: {xml_file}')
        quit()

    mtime = localtime(os.path.getmtime(xml_file))
    timestamp = strftime('%Y%m%d', mtime)

    caminho = os.path.dirname(xml_file) + "\\output\\"
    output = os.path.splitext(xml_file)[0] + ".xlsx"

    # Build Output Filename
    i = 0
    while os.path.exists(output):
        i = i + 1
        output = os.path.splitext(xml_file)[0] + " (" + str(i) + ").xlsx"    

    print('\n# Parse Start...\n')
    nokr.process(xml_file, caminho, READ_TYPE, default_list)

    tm_parse = perf_counter()
    print("\n# Merging data...\n")

    MergeCSV(caminho, output)

    tm_merge = perf_counter()
    te_parse = round(tm_parse - tm_start , 2)
    te_merge = round(tm_merge - tm_parse , 2)

    print(f'    Read : {te_parse:7.2f} s')
    print(f'    Merge: {te_merge:7.2f} s')

    te_all = round(tm_merge - tm_start , 2)
    print(f'           ----------\n    Total: {te_all:7.2f} s')

    print("\n# Finished!\n\n  ==> " + output)