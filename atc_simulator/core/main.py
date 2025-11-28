import sys
from PySide6.QtWidgets import QApplication

from espace_aerien import EspaceAerien
from score_manager import ScoreManager
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    espace = EspaceAerien(taille=100)
    score = ScoreManager()

    fenetre = MainWindow(espace, score, tick_ms=100)
    fenetre.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
