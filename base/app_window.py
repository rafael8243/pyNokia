
import tkinter as tk

class reader_window(tk.Tk):
    def __init__(self, app):
        super().__init__()
        self.title('NOKIA Parser 2')
        self._app = app
        self._create_board_display()
        #self._create_board_grid()

    def _create_board_display(self):
        self.geometry(self._app.board_size)

        self.toolbar_box = tk.Frame(master=self, relief="ridge", bd=0)
        self.toolbar_box.pack(fill=tk.X, expand=None, side="top", anchor="n", padx=10, pady=(10,0))

        # Frame 2
        self.content_box = tk.Frame(master=self, relief="ridge", bd=0)
        self.content_box.pack(fill="x", expand=None, side="bottom", anchor="n")

        btn_open = tk.Button(self.toolbar_box, text="Open XML")
        btn_open["command"] = self.select_file
        btn_open.pack(side="left")

        rad_def = tk.Radiobutton(self.toolbar_box, text="Default", variable=self._app.READ_TYPE, value="DEFAULT")
        rad_all = tk.Radiobutton(self.toolbar_box, text="Complete", variable=self._app.READ_TYPE, value="READALL")
        rad_def.pack(side="right")
        rad_all.pack(side="right")

        self.txt_out = tk.Text(self.content_box, height = 19, width = 130)
        self.txt_out.pack(side="top", padx=10, pady=10)
        self.txt_out.insert(tk.END,'teste')


    def print_box(self, s):
        self.txt_out.insert(tk.END, s)


    def select_file(self):

        filetypes = (
            ('XML files', '*.xml'),
            ('All files', '*.*')
        )

        xml_files_path = tk.filedialog.askopenfilenames(
            title='Open XML DUMP',
            initialdir=self._app.base_path,
            filetypes=filetypes)

        if self._app.check_file(xml_files_path):

            txt = [f'\n - {x}' for x in self._app.xml_files_info]
            self.print_box(txt[0])
            
            self.print_box(f'\n\n# Processing: {self._app.READ_TYPE}')
            #self.lbl_file = Label(self.content_box, text=self.xml_file_path).pack(side="bottom")

            self._app.threading_read()
            print("sair2")
