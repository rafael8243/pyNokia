from tkinter import (Button, Radiobutton, Frame, Label, StringVar, Tk, filedialog)
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

import pandas as pd
import tempfile
from pathlib import Path
from threading import Thread
from queue import Queue

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
        self.base_path = str(Path.home() / 'Documents')
        
        # Thread-safe message queue for background thread communication
        self.message_queue = Queue()
        self.is_processing = False

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
        
        # Start monitoring message queue for thread-safe GUI updates
        self.check_message_queue()


    def print_box(self, text: str):
        """Display text in output box (main thread only)."""
        self.txt_out.insert('end', text)
        self.txt_out.see('end')
    
    def queue_message(self, text: str):
        """Thread-safe: background threads call this to send messages to GUI."""
        self.message_queue.put(text)
    
    def check_message_queue(self):
        """Check queue for messages from background threads (runs on main thread).
        
        Periodically processes all queued messages and updates GUI safely.
        This avoids race conditions by keeping all GUI updates on the main thread.
        Runs continuously on the main thread via after() callback.
        """
        try:
            # Process all queued messages without blocking
            while True:
                msg = self.message_queue.get_nowait()
                self.print_box(msg)
        except:
            # Queue is empty, which is normal - this is not an error
            pass
        
        # Always schedule next check - keep monitoring continuously
        # This ensures messages are picked up as soon as they're queued
        self.after(100, self.check_message_queue)


    def check_file(self) -> bool:

        self.print_box(f'\n\n###############################################################\n\n# Source file(s):')

        for i in range(len(self.xml_files_path)):
            file_path = Path(self.xml_files_path[i])

            if file_path.exists():
                # Update base directory to last used
                self.base_path = str(file_path.parent)
                xml_size = round(file_path.stat().st_size / (1024 * 1024), 2)
                self.print_box(f'\n  - {file_path.name} ({xml_size} MB)')

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
            self.is_processing = True
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
        """Background thread: reads XML files and exports to Excel.
        
        Uses self.message_queue to safely communicate with GUI thread.
        All print_box() calls replaced with queue_message() for thread safety.
        """
        from base import nok_etreader as nokr
        from time import perf_counter

        try:
            default_list = ['LNCEL_FDD', 'LNBTS', 'LNCEL', 'IRFIM', 'SIB', 'LNMME','MOPR',
                            'LNADJW', 'LNADJG', 'LNHOIF', 'CAREL', 'LNBTS_FDD', 'WNCELG', 'WNBTS',
                            'ADJI', 'WBTS', 'ADJS', 'ADJD', 'WCEL', 'FMCS', 'HOPS', 
                            'COCO', 'ADJG', 'ADJL', 'RNC', 'LAPD', 'MAL', 'TRX', 
                            'BCF', 'DAP', 'BTS', 'ADCE', 'ADJW', 'BAL', 'BSC']

            # Build Output Filename
            temp_path = tempfile.TemporaryDirectory(prefix='_dn')
            self.tmp_path = temp_path.name

            source_file = Path(self.xml_files_path[0])
            out_file = source_file.with_suffix('.xlsx')

            # Remove Nokia dump identifiers from filename
            filename = out_file.stem
            for old, new in (("NOK3", "DUMP"), ("NOK4", "DUMP"), ("NOK5", "DUMP")):
                filename = filename.replace(old, new)
            out_file = out_file.parent / f"{filename}.xlsx"

            # Auto-increment filename if it already exists
            i = 0
            while out_file.exists():
                i += 1
                out_file = out_file.parent / f"{filename} ({i}).xlsx"

            # Clean temporary output directory
            tmp_path = Path(self.tmp_path)
            for csv_file in tmp_path.glob('*.csv'):
                csv_file.unlink()

            tm_start = perf_counter()

            # Create thread-safe callback for subprocess logging
            def thread_safe_print(msg: str):
                """Callback for background threads to queue messages safely."""
                self.queue_message(msg)

            # Read and export selected elements
            nokr.process(self.xml_files_path, self.tmp_path, self.fread_type, 
                        default_list, thread_safe_print)

            tm_parse = perf_counter()
            self.queue_message('\n\n  >> MAKE EXCEL EXPORT...')

            MergeCSV(self.tmp_path, str(out_file), thread_safe_print)

            tm_merge = perf_counter()
            te_parse = round(tm_parse - tm_start , 2)
            te_merge = round(tm_merge - tm_parse , 2)
            te_all   = round(tm_merge - tm_start , 2)

            self.queue_message(f'\n  Read : {te_parse:7.2f} s')
            self.queue_message(f'\n  Merge: {te_merge:7.2f} s')
            self.queue_message(f'\n         ----------\n  Total: {te_all:7.2f} s')
            self.queue_message(f"\n\n  >> FINISHED\n      - {out_file}\n")
            
        except Exception as e:
            # Catch any errors and display them safely to user
            self.queue_message(f'\n\n  >> ERROR DURING PROCESSING <<\n')
            self.queue_message(f'  {type(e).__name__}: {str(e)}\n')
            self.queue_message(f'  Please check your XML file and try again.\n')
            import traceback
            self.queue_message(f'\n  Details: {traceback.format_exc()}\n')
        
        finally:
            # Always mark processing as complete
            self.is_processing = False


if __name__ == '__main__':

    def MergeCSV(origem, destino, fprint):
        """Merge multiple CSV files into a single Excel workbook.
        
        Args:
            origem (str): Source directory containing CSV files
            destino (str): Output Excel file path
            fprint (callable): Thread-safe callback for logging messages
        
        Raises:
            FileNotFoundError: If origin directory doesn't exist
            IOError: If there are problems reading/writing files
        """
        origem_path = Path(origem)
        
        if not origem_path.exists():
            raise FileNotFoundError(f"Source directory not found: {origem}")
        
        csv_list = list(origem_path.glob('*.csv'))

        fprint(f"\n\n# Saving output file...")

        # Use context manager to ensure ExcelWriter is properly closed
        # even if an exception occurs during processing

        with pd.ExcelWriter(destino) as writer:
            for csv_file in csv_list:
                try:
                    df = pd.read_csv(str(csv_file), delimiter='|', encoding='iso-8859-1')
                    sname = csv_file.stem
                    fprint(f'\n    {sname} - OK')
                    
                    df.to_excel(writer, sheet_name=sname, index=False)
                except Exception as e:
                    fprint(f'\n    ERROR reading {csv_file.name}: {str(e)}')
                    # Continue processing other files
                    continue
        
        fprint("\n\n# Done!\n")

    app = App()
    app.start()
