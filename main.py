#NAMA: AZIZAH INDRIANI PUTRI
#NIM: F1D02310041
#KELAS: D

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
