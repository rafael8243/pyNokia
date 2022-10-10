import os
import sys
import pandas as pd
from time import perf_counter, localtime, strftime

import nok_etreader as nokr


def MergeCSV(origem, destino):

    csv_list = [origem + f for f in os.listdir(origem)]

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

    tm_start = perf_counter()

    # Get XML Filename
    xml_file = "C:\\Users\\oi399542\\Documents\\base_DUMPs\\dump_sample.xml"
    if len(sys.argv) == 2: xml_file = sys.argv[1]   #get file from command line

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
    nokr.process(xml_file, caminho)

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