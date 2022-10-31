import os
from tkinter import Tk

from base import app_view

class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        app_view.begin(self)
        self.mainloop()


if __name__ == '__main__':

    App()