# -*- coding: utf-8 -*-
import sys
from PySide6.QtWidgets import QApplication
from gui import Window


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
