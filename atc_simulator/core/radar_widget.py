from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QRectF, Signal
import math


class RadarWidget(QWidget):
    avion_selectionne_radar = Signal(str)

    def __init__(self, espace_aerien, taille, parent=None):
        super().__init__(parent)
        self.espace = espace_aerien
        self.taille = taille
        self.setMinimumSize(400, 400)

    def sim_to_px(self, x, y):

        px = (x / self.taille) * self.width()
        py = (1 - y / self.taille) * self.height()
        return px, py

    def px_to_sim(self, px, py):
        """Convertit des pixels en coordonnées logiques (0..taille)."""
        x = px / self.width() * self.taille
        y = (1 - py / self.height()) * self.taille
        return x, y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("black"))


        cx = self.width() / 2
        cy = self.height() / 2

        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.setPen(QColor("green"))
        marge = 10

        painter.drawText(cx - 20, marge + 15, "N 0°")
        painter.drawText(cx - 30, self.height() - marge, "S 180°")
        painter.drawText(self.width() - 70, cy - 5, "E 90°")
        painter.drawText(marge, cy - 5, "O 270°")


        zx, zy, zw, zh = self.espace.zone_atterrissage
        x1, y1 = self._sim_to_px(zx, zy)
        x2, y2 = self._sim_to_px(zx + zw, zy + zh)
        rect = QRectF(x1, y2, x2 - x1, y1 - y2)  # inversion Y

        painter.setPen(QPen(QColor("green"), 2, Qt.DashLine))
        painter.drawRect(rect)


        for avion in self.espace.liste_avions:
            px, py = self._sim_to_px(avion.x, avion.y)

            if avion.selectionne:
                color = QColor("white")
            else:
                color = QColor("cyan")

            painter.setPen(QPen(color, 2))
            painter.setBrush(color)
            painter.drawEllipse(int(px) - 4, int(py) - 4, 8, 8)

            painter.setFont(QFont("Arial", 9))
            painter.drawText(int(px) + 6, int(py) - 2, avion.id_vol)
            painter.drawText(int(px) + 6, int(py) + 10, f"{avion.altitude} m")

        painter.end()

    def mousePressEvent(self, event):

        try:
            pos = event.position()
            px, py = pos.x(), pos.y()
        except AttributeError:
            pos = event.pos()
            px, py = pos.x(), pos.y()

        x, y = self._px_to_sim(px, py)


        for avion in self.espace.liste_avions:
            dist = math.hypot(avion.x - x, avion.y - y)
            if dist < 3:
                self.avion_selectionne_radar.emit(avion.id_vol)
                break

