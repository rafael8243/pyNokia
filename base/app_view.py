import os
import pandas as pd
from time import perf_counter, localtime, strftime
from threading import Thread

import tkinter as tk
from tkinter import ttk
from tkinter import (Button, Radiobutton, Text, Frame, IntVar, Label, 
                     Listbox, Menu, StringVar, Tk, filedialog)

from base import nok_etreader as nokr

class begin():

    def __init__(self, master):
        self.root = master

        self.root.title('NOKIA Parser')
        self.root.resizable(False, False)
        self.root.geometry('450x150')
        
        # set_window_center(self.root, 900, 600)
        self.root.update()

        self.xmlfile = StringVar(value="C:/C/75_dump/2G_NOK5-20230306.xml")
        self.READ_TYPE = StringVar(value="DEFAULT")

        self.toolbar_box = None
        self.content_box = None

        self.init_view()

    def init_view(self):
        """Build interface"""

        # Frame 1
        self.toolbar_box = Frame(self.root, relief="ridge", bd=1)
        self.toolbar_box.pack(fill="x", expand=None, side="top", anchor="n")

        # Frame 2        
        self.content_box = Frame(self.root, relief="ridge", bd=1)
        self.content_box.pack(fill="x", expand=None, side="bottom", anchor="n")        

        btn_open = Button(self.toolbar_box, text="Open XML")
        btn_open["command"] = self.select_file
        btn_open.pack(side="left")

        rad_def = Radiobutton(self.toolbar_box, text="Default", variable=self.READ_TYPE, value="DEFAULT")
        rad_all = Radiobutton(self.toolbar_box, text="Complete", variable=self.READ_TYPE, value="READALL")
        rad_def.pack(side="right")
        rad_all.pack(side="right")

        self.txt_out = Text(self.content_box, height = 10, width = 130)
        self.txt_out.pack(side="bottom")

        openfile = self.xmlfile.get()
        self.lbl_file = Label(self.content_box, text=openfile).pack(side="bottom")



    def select_file(self):
        filetypes = (
            ('XML files', '*.xml'),
            ('All files', '*.*')
        )

        self.xmlFile = filedialog.askopenfilename(
            title='Open XML DUMP',
            initialdir='C:/C/75_dump/',
            filetypes=filetypes)
        
        self.check_file(self.xmlFile)

        self.fread_type = self.READ_TYPE.get()
        self.print_box(f'\n# Processing: {self.fread_type}')
        self.read_file(self.xmlFile)


    def print_box(self, s):
        self.txt_out.insert(tk.END, s)


    def check_file(self, xml_file):

        path_split = os.path.split(xml_file)

        if os.path.exists(xml_file):
            xml_size = round(os.stat(xml_file).st_size / (1024 * 1024),2)
            self.print_box(f'\n# Source file:\n  + {path_split[1]} ({xml_size} MB)')

        else:
            self.print_box(f'\n# File NOT found:\n  + {xml_file}')
            quit()

    def read_file(self, xml_file):

        tm_start = perf_counter()
        
        default_list = ['LNCEL_FDD', 'LNBTS', 'LNADJ', 'LNCEL', 'IRFIM', 'SIB', 'LNADJL', 
        'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'LNBTS_FDD', 'ADJI', 'WBTS', 'ADJS', 
        'ADJD', 'WCEL', 'FMCS', 'HOPS', 'COCO', 'ADJG', 'ADJL', 'RNC', 'LAPD', 
        'MAL', 'TRX', 'BCF', 'ADJL', 'DAP', 'BTS', 'CSDAP', 'ADCE', 'ADJW', 'BAL',
        'BSC', 'LNMME','MOPR']

        mtime = localtime(os.path.getmtime(xml_file))
        timestamp = strftime('%Y%m%d', mtime)

        caminho = os.path.dirname(xml_file) + "/output/"
        output = os.path.splitext(xml_file)[0] + ".xlsx"

        # Build Output Filename
        i = 0
        while os.path.exists(output):
            i = i + 1
            output = os.path.splitext(xml_file)[0] + " (" + str(i) + ").xlsx"    

        # Read and export selected elements 
        nokr.process(xml_file, caminho, self.fread_type, default_list)

        tm_parse = perf_counter()
        self.print_box('\n# Merging data...')

        MergeCSV(caminho, output)

        tm_merge = perf_counter()
        te_parse = round(tm_parse - tm_start , 2)
        te_merge = round(tm_merge - tm_parse , 2)

        self.print_box(f'  Read : {te_parse:7.2f} s')
        self.print_box(f'  Merge: {te_merge:7.2f} s')

        te_all = round(tm_merge - tm_start , 2)
        self.print_box(f'         ----------\n    Total: {te_all:7.2f} s')

        self.print_box("\n# Finished!\n\n  ==> " + output)


def MergeCSV(origem, destino):
    
    files = os.listdir(origem)
    csv_list = [origem + i for i in files if i.endswith('.csv')]

    print(f"  + Found {len(csv_list)} element types:\n")

    writer = pd.ExcelWriter(destino) # Arbitrary output name

    for csvfilename in csv_list:

        df = pd.read_csv(csvfilename, engine='python', delimiter=';')     #TODO Guess field type
        sname = csvfilename.split('/')[-1].split('.')[0]
        print(f'    {sname} - OK')
        
        df.to_excel(writer, sheet_name=sname, index = False)
    
    print("\n# Saving output file...\n")
    writer.close()