import PySimpleGUI as sg

from gui.main_layout import MainLayout


def main() -> None:
    layout = MainLayout()
    window = layout.create_window()
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

    window.close()


if __name__ == "__main__":
    main()
