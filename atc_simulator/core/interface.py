import sys
from PySide6.QtWidgets import QApplication, QWidget


class Fenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATC")
        self.resize(900, 600)
        self.setStyleSheet("background-color: #000;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Fenetre()
    w.show()
    sys.exit(app.exec())
