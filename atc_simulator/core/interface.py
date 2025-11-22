from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QListWidgetItem, QLabel, QGroupBox, QStatusBar
)
from PySide6.QtCore import Qt, Signal, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QFont


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


class RadarWidget(QWidget):
    avion_selectionne_radar = Signal(str)

    def __init__(self, espace_aerien, radar_range_km, parent=None):
        super().__init__(parent)
        self.espace_aerien = espace_aerien
        self.radar_range_km = radar_range_km
        self.setMinimumSize(400, 400)

    def _convertir_coords_pixels(self, sim_x, sim_y):
        pixel_x = (sim_x / self.radar_range_km) * self.width()
        pixel_y = (1 - (sim_y / self.radar_range_km)) * self.height()
        return pixel_x, pixel_y

    def _convertir_pixels_coords(self, pixel_x, pixel_y):
        sim_x = (pixel_x / self.width()) * self.radar_range_km
        sim_y = (1 - (pixel_y / self.height())) * self.radar_range_km
        return sim_x, sim_y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("black"))

        zx, zy, zw, zh = self.espace_aerien.zone_atterrissage
        px, py = self._convertir_coords_pixels(zx, zy + zh)
        px_w, px_h = self._convertir_coords_pixels(zx + zw, zy)
        landing_rect = QRectF(px, py, px_w - px, px_h - py)
        painter.setPen(QPen(QColor("green"), 2, Qt.PenStyle.DashLine))
        painter.drawRect(landing_rect)

        for avion in self.espace_aerien.liste_avions:
            px, py = self._convertir_coords_pixels(avion.x, avion.y)

            if avion.statut == "urgence":
                pen_color = QColor("red")
            elif avion.selectionne:
                pen_color = QColor("white")
            else:
                pen_color = QColor("blue")

            painter.setPen(QPen(pen_color, 2))
            painter.setBrush(pen_color)
            painter.drawEllipse(int(px) - 4, int(py) - 4, 8, 8)

            painter.setFont(QFont("Arial", 9))
            painter.drawText(int(px) + 8, int(py) + 5, f"{avion.id_vol}")
            painter.drawText(int(px) + 8, int(py) + 18, f"{avion.altitude}m")

        painter.end()

    def mousePressEvent(self, event):
        clic_x, clic_y = event.position().x(), event.position().y()
        sim_x, sim_y = self._convertir_pixels_coords(clic_x, clic_y)

        import math
        for avion in self.espace_aerien.liste_avions:
            dist = math.sqrt((avion.x - sim_x) ** 2 + (avion.y - sim_y) ** 2)
            if dist < 3:
                self.avion_selectionne_radar.emit(avion.id_vol)
                return


class MainWindow(QMainWindow):
    def __init__(self, espace_aerien, score_manager, config, parent=None):
        super().__init__(parent)

        self.espace_aerien = espace_aerien
        self.score_manager = score_manager

        self.setWindowTitle(config.get("window_title", "ATC Sim"))
        self.resize(config["window_size"][0], config["window_size"][1])
        self.setStatusBar(QStatusBar(self))

        self.info_panel = InfoPanel()
        self.radar_widget = RadarWidget(
            self.espace_aerien,
            config.get("radar_range_km", 100)
        )

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.info_panel, 1)
        main_layout.addWidget(self.radar_widget, 3)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
