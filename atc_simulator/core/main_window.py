from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStatusBar
)
from PySide6.QtCore import QTimer

from info_panel import InfoPanel
from radar_widget import RadarWidget
from controls_panel import ControlsPanel


class MainWindow(QMainWindow):
    def __init__(self, espace_aerien, score_manager, tick_ms=100):
        super().__init__()

        self.espace = espace_aerien
        self.score_manager = score_manager
        self.tick_ms = tick_ms

        self.setWindowTitle("Simulateur ATC")
        self.resize(1100, 700)
        self.setStatusBar(QStatusBar(self))


        self.info_panel = InfoPanel()
        self.radar = RadarWidget(self.espace, self.espace.taille)
        self.controls = ControlsPanel()


        central = QWidget()
        layout = QHBoxLayout(central)
        layout.addWidget(self.info_panel, 1)
        layout.addWidget(self.radar, 3)
        layout.addWidget(self.controls, 1)
        self.setCentralWidget(central)


        self.info_panel.avion_selectionne.connect(self.selectionner_par_id)
        self.radar.avion_selectionne_radar.connect(self.selectionner_par_id)
        self.controls.instruction_cap.connect(self.changer_cap)
        self.controls.instruction_altitude.connect(self.changer_altitude)
        self.controls.instruction_atterrir.connect(self.autoriser_atterrissage)


        self.timer_tick = QTimer(self)
        self.timer_tick.timeout.connect(self.tick)

        self.timer_spawn = QTimer(self)
        self.timer_spawn.timeout.connect(self.espace.ajouter_avion)

        self.demarrer_simulation()

    def demarrer_simulation(self):
        self.espace.ajouter_avion()
        self.timer_tick.start(self.tick_ms)
        self.timer_spawn.start(8000)  # un avion toutes les 8 secondes


    def selectionner_par_id(self, id_vol: str):
        avion = self.espace.selectionner_par_id(id_vol)
        self.controls.set_avion(avion)

    def changer_cap(self, cap: int):
        avion = self.espace.get_avion_selectionne()
        if avion:
            avion.changer_cap(cap)

    def changer_altitude(self, alt: int):
        avion = self.espace.get_avion_selectionne()
        if avion:
            avion.changer_altitude(alt)

    def autoriser_atterrissage(self):
        avion = self.espace.get_avion_selectionne()
        if avion:
            avion.demarrer_atterrissage()
            self.statusBar().showMessage(
                f"{avion.id_vol} autorisé à l'atterrissage",
                3000
            )



    def tick(self):
        self.espace.mettre_a_jour(self.tick_ms)

        if self.espace.detecter_collisions():
            self.score_manager.appliquer_evenement("collision")
            self.statusBar().showMessage("Collision détectée !", 3000)


        reussi, crash_sol = self.espace.gerer_atterrissages()

        if reussi:
            self.score_manager.appliquer_evenement("atterrissage")
            self.statusBar().showMessage("Atterrissage réussi !", 3000)

        if crash_sol:
            self.score_manager.appliquer_evenement("collision")
            self.statusBar().showMessage(
                "Atterrissage raté : hors de la piste !",
                3000
            )

        self.espace.nettoyer_avions()


        self.radar.update()
        self.info_panel.maj_stats(self.score_manager, self.espace)
        self.info_panel.maj_liste_avions(self.espace.liste_avions)


        if self.espace.get_avion_selectionne() is None:
            self.controls.set_avion(None)
