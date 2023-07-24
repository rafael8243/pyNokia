from tkinter import Tk
from base import app_view
from base import app_window, app_reader

class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        app_view.begin(self)
        self.mainloop()

def main():
    """Create the board and run its main loop."""
    app = app_reader.nokia_parser()
    board = app_window.reader_window(app)
    board.mainloop()

if __name__ == "__main__":
    main()

    #App()