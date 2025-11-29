from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel,
    QListWidget, QListWidgetItem
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
        self.lbl_score = QLabel("Score : 0")
        self.lbl_collisions = QLabel("Collisions : 0")
        self.lbl_atterrissages = QLabel("Atterrissages : 0")
        stats_layout.addWidget(self.lbl_score)
        stats_layout.addWidget(self.lbl_collisions)
        stats_layout.addWidget(self.lbl_atterrissages)
        stats_group.setLayout(stats_layout)


        avions_group = QGroupBox("AVIONS EN VOL")
        avions_layout = QVBoxLayout()
        self.liste_avions_widget = QListWidget()
        self.liste_avions_widget.itemClicked.connect(self.on_avion_clique)
        avions_layout.addWidget(self.liste_avions_widget)
        avions_group.setLayout(avions_layout)

        layout.addWidget(stats_group)
        layout.addWidget(avions_group)
        layout.addStretch()

    def on_avion_clique(self, item: QListWidgetItem):
        id_vol = item.data(Qt.UserRole)
        self.avion_selectionne.emit(id_vol)

    def maj_stats(self, score_manager, espace_aerien):
        self.lbl_score.setText(f"Score : {score_manager.score}")
        self.lbl_collisions.setText(f"Collisions : {espace_aerien.collisions_detectees}")
        self.lbl_atterrissages.setText(
            f"Atterrissages : {espace_aerien.atterrissages_reussis}"
        )

    def maj_liste_avions(self, avions):
        self.liste_avions_widget.clear()
        for avion in avions:
            texte = f"{avion.id_vol} | Alt : {avion.altitude} m"
            item = QListWidgetItem(texte)
            item.setData(Qt.UserRole, avion.id_vol)

            if avion.selectionne:
                item.setBackground(QColor("blue"))

            self.liste_avions_widget.addItem(item)
