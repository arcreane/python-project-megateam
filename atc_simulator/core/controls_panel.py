from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont


class ControlsPanel(QWidget):
    instruction_cap = Signal(int)
    instruction_altitude = Signal(int)
    instruction_atterrir = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.lbl_selection = QLabel("Aucun avion sélectionné")
        self.lbl_selection.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.lbl_selection)

        group = QGroupBox("Ordres")
        form = QFormLayout()

        self.txt_cap = QLineEdit()
        self.btn_cap = QPushButton("Changer cap")
        form.addRow("Cap (0-360°) :", self.txt_cap)
        form.addRow(self.btn_cap)

        self.txt_alt = QLineEdit()
        self.btn_alt = QPushButton("Changer altitude")
        form.addRow("Altitude (m) :", self.txt_alt)
        form.addRow(self.btn_alt)

        group.setLayout(form)
        layout.addWidget(group)

        self.btn_atterrir = QPushButton("Autoriser atterrissage")
        layout.addWidget(self.btn_atterrir)
        layout.addStretch()


        self.btn_cap.clicked.connect(self.on_cap)
        self.btn_alt.clicked.connect(self.on_alt)
        self.btn_atterrir.clicked.connect(self.on_atterrir)

        self._set_actif(False)

    def _set_actif(self, actif: bool):
        self.btn_cap.setEnabled(actif)
        self.btn_alt.setEnabled(actif)
        self.btn_atterrir.setEnabled(actif)
        self.txt_cap.setEnabled(actif)
        self.txt_alt.setEnabled(actif)

    def set_avion(self, avion):
        if avion is None:
            self.lbl_selection.setText("Aucun avion sélectionné")
            self.txt_cap.clear()
            self.txt_alt.clear()
            self._set_actif(False)
        else:
            self.lbl_selection.setText(f"Sélection : {avion.id_vol}")
            self.txt_cap.setText(str(avion.cap))
            self.txt_alt.setText(str(avion.altitude))
            self._set_actif(True)

    def on_cap(self):
        try:
            cap = int(self.txt_cap.text())
        except ValueError:
            return
        self.instruction_cap.emit(cap)

    def on_alt(self):
        try:
            alt = int(self.txt_alt.text())
        except ValueError:
            return
        self.instruction_altitude.emit(alt)

    def on_atterrir(self):
        self.instruction_atterrir.emit()

