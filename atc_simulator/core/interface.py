
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QListWidgetItem, QLabel, QGroupBox, QStatusBar
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor


class InfoPanel(QWidget):

    avion_selectionne = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        stats_group = QGroupBox("STATS")
        stats_layout = QVBoxLayout()
        self.lbl_score = QLabel("Score: 0")
        self.lbl_collisions = QLabel("Collisions: 0")
        stats_layout.addWidget(self.lbl_score)
        stats_layout.addWidget(self.lbl_collisions)
        stats_group.setLayout(stats_layout)


        avions_group = QGroupBox("AVIONS EN VOL")
        avions_layout = QVBoxLayout()
        self.liste_avions_widget = QListWidget()
        self.liste_avions_widget.itemClicked.connect(self.on_avion_clique)
        avions_layout.addWidget(self.liste_avions_widget)
        avions_group.setLayout(avions_layout)

        layout.addWidget(stats_group)
        layout.addWidget(avions_group)

    def on_avion_clique(self, item: QListWidgetItem):

        id_vol = item.data(Qt.ItemDataRole.UserRole)
        self.avion_selectionne.emit(id_vol)

    def update_stats(self, score_manager, espace_aerien):

        self.lbl_score.setText(f"Score: {score_manager.score_actuel}")
        self.lbl_collisions.setText(f"Collisions: {espace_aerien.collisions_detectees}")

    def update_liste_avions(self, avions):

        self.liste_avions_widget.clear()
        for avion in avions:
            texte = f"{avion.id_vol} | {avion.altitude}m | {avion.carburant:.0f}%"
            item = QListWidgetItem(texte)
            item.setData(Qt.ItemDataRole.UserRole, avion.id_vol)

            if avion.statut == "urgence":
                item.setForeground(QColor("red"))
            if avion.selectionne:
                item.setBackground(QColor("blue"))

            self.liste_avions_widget.addItem(item)


class MainWindow(QMainWindow):


    def __init__(self, espace_aerien, score_manager, config, parent=None):
        super().__init__(parent)


        self.espace_aerien = espace_aerien
        self.score_manager = score_manager

        self.setWindowTitle(config.get("window_title", "ATC Sim"))
        self.resize(config["window_size"][0], config["window_size"][1])
        self.setStatusBar(QStatusBar(self))

        self.info_panel = InfoPanel()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.info_panel, 1)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
