from base import app_window, app_reader

def MainApp():
    """Create the board and run its main loop."""

    app = app_reader.nokia_parser()
    board = app_window.reader_window(app)
    board.mainloop()

if __name__ == "__main__":

    MainApp()