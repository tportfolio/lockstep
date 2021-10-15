import PySimpleGUI as sg

from src.gui.main_layout import MainLayout
from src.gui.callbacks import Callbacks


def main() -> None:
    layout = MainLayout()
    window = layout.create_window()
    callbacks = Callbacks(window)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif callbacks.has_callback(event):
            callbacks.execute_callback(event, values)
        else:
            print(f"Unexpected key: {event}")

    window.close()


if __name__ == "__main__":
    main()
