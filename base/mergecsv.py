import pandas as pd
import os

def MergeCSV(origem, destino):

    csv_list = [origem + f for f in os.listdir(origem)]

    print("Found %d files..." % len(csv_list))

    writer = pd.ExcelWriter(destino) # Arbitrary output name
    for csvfilename in csv_list:        
        df = pd.read_csv(csvfilename, engine='python', delimiter=',') 
        sname = csvfilename.split('\\')[-1].split('.')[0]
        df.to_excel(writer,sheet_name=sname, index = False)
        
    writer.close()
