from tkinter import (Button, Radiobutton, Frame, Label, StringVar, Tk, filedialog)
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

import pandas as pd
import tempfile

import os.path
from threading import Thread

class App(Tk):

    APP_NAME = "NOKIA Parser II"
    WIDTH = 550
    HEIGHT = 600

    def __init__(self):
        Tk.__init__(self)
        style = ttk.Style(self)
        style.theme_use('clam')
        #app_view.begin(self)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.READ_TYPE = StringVar(value="DEFAULT")
        self.xml_file_path = StringVar(value="")
        self.base_path = os.path.expanduser('~/Documents')

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Frame 1
        toolbar_box = ttk.Frame(self, relief="ridge")
        toolbar_box.pack(fill="x", side="top", padx=5, pady=5)

        # Frame 2
        content_box = ttk.Frame(self, relief="ridge")
        content_box.pack(fill="both", side='top', padx=5, pady=(0,5), expand=True)

        btn_open = ttk.Button(toolbar_box, text="Open XML", command=self.select_file)
        btn_open.pack(side="left", padx=5, pady=5)

        rad_def = ttk.Radiobutton(toolbar_box, text="Default" , variable=self.READ_TYPE, value="DEFAULT")
        rad_all = ttk.Radiobutton(toolbar_box, text="Complete", variable=self.READ_TYPE, value="READALL")
        rad_def.pack(side="right", padx=10)
        rad_all.pack(side="right")

        self.txt_out = ScrolledText(content_box, height=300, bg='lightgray')
        self.txt_out.pack(fill="both", padx=5, pady=5)
        self.print_box('Open XML file to begin.')

        self.xml_file_path.get()


    def print_box(self, text:str):
        self.txt_out.insert('end', text)
        self.txt_out.see('end')


    def check_file(self) -> bool:

        self.print_box(f'\n\n###############################################################\n\n# Source file(s):')

        for i in range(len(self.xml_files_path)):
            path_split = os.path.split(self.xml_files_path[i])

            if os.path.exists(self.xml_files_path[i]):
                self.base_path = os.chdir(path_split[0]) # Change base directory to last used
                xml_size = round(os.path.getsize(self.xml_files_path[i]) / (1024 * 1024),2)
                self.print_box(f'\n  - {path_split[1]} ({xml_size} MB)')

            else:
                self.print_box(f'\n  >> FILE NOT FOUND: {self.xml_files_path[i]} <<')
                return False

        return True


    def select_file(self):
        filetypes = (
            ('XML files', '*.xml'),
            ('All files', '*.*')
        )

        self.xml_files_path = filedialog.askopenfilenames(
            title='Open XML DUMP',
            initialdir=self.base_path,
            filetypes=filetypes)

        if len(self.xml_files_path) == 0:
            self.print_box('  >> NO FILE SELECTED <<')
            return False

        if self.check_file():
            self.fread_type = self.READ_TYPE.get()
            self.threading_read()


    def start(self):
        self.mainloop()


    def on_closing(self, event=0):
        self.destroy()


    def threading_read(self):

        # Call work function
        t1=Thread(target = self.read_file)
        t1.start()


    def read_file(self):
        from base import nok_etreader as nokr
        from time import perf_counter

        default_list = ['LNCEL_FDD', 'LNBTS', 'LNCEL', 'IRFIM', 'SIB', 'LNMME','MOPR',
                        'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'LNBTS_FDD', 'WNCELG', 'WNBTS',
                        'ADJI', 'WBTS', 'ADJS', 'ADJD', 'WCEL', 'FMCS', 'HOPS', 
                        'COCO', 'ADJG', 'ADJL', 'RNC', 'LAPD', 'MAL', 'TRX', 
                        'BCF', 'DAP', 'BTS', 'ADCE', 'ADJW', 'BAL', 'BSC']


        # Build Output Filename
        temp_path = tempfile.TemporaryDirectory(prefix='_dn')
        self.tmp_path = temp_path.name

        out_file = os.path.splitext(self.xml_files_path[0])[0] + ".xlsx"

        for r in (("NOK3", "DUMP"), ("NOK4", "DUMP"), ("NOK5", "DUMP")):
            out_file = out_file.replace(*r)

        i = 0
        while os.path.exists(out_file):
            i +=  1
            out_file = os.path.split(out_file)[0] + " (" + str(i) + ").xlsx"


        # Limpa parta temporária de saída
        old_files = os.listdir(self.tmp_path)
        for f in old_files:
            if f.endswith(".csv"):
                os.remove(os.path.join(self.tmp_path, f))

        tm_start = perf_counter()

        # Read and export selected elements
        nokr.process(self.xml_files_path, self.tmp_path, self.fread_type, default_list, self.print_box)

        tm_parse = perf_counter()
        self.print_box('\n\n  >> MAKE EXCEL EXPORT...')

        MergeCSV(self.tmp_path, out_file, self.print_box)

        tm_merge = perf_counter()
        te_parse = round(tm_parse - tm_start , 2)
        te_merge = round(tm_merge - tm_parse , 2)
        te_all   = round(tm_merge - tm_start , 2)

        self.print_box(f'\n  Read : {te_parse:7.2f} s')
        self.print_box(f'\n  Merge: {te_merge:7.2f} s')
        self.print_box(f'\n         ----------\n  Total: {te_all:7.2f} s')
        self.print_box(f"\n\n  >> FINISHED\n      - {out_file}\n")


if __name__ == '__main__':

    def MergeCSV(origem, destino, fprint):
        
        files = os.listdir(origem)
        csv_list = [f'{origem}/{i}' for i in files if i.endswith('.csv')]

        fprint(f"\n\n# Saving output file...")

        writer = pd.ExcelWriter(destino) # Arbitrary output name

        for csvfilename in csv_list:

            df = pd.read_csv(csvfilename, engine='python', delimiter='|', encoding='iso-8859-1')     #TODO Guess field type
            sname = csvfilename.split('/')[-1].split('.')[0]
            fprint(f'\n    {sname} - OK')
            
            df.to_excel(writer, sheet_name=sname, index=False)
        
        writer.close()
        fprint("\n\n# Done!\n")

    app = App()
    app.start()
