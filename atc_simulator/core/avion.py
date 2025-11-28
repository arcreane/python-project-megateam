import math

class Avion:
    def __init__(self, id_vol, x, y, altitude, vitesse, cap):
        self.id_vol = id_vol
        self.x = x
        self.y = y
        self.altitude = altitude
        self.vitesse = vitesse
        self.cap = cap
        self.statut = "en-vol"
        self.selectionne = False

    def changer_cap(self, nouveau_cap: int):
        self.cap = nouveau_cap % 360

    def changer_altitude(self, nouvelle_altitude: int):
        if nouvelle_altitude < 0:
            nouvelle_altitude = 0
        self.altitude = nouvelle_altitude

    def demarrer_atterrissage(self):
        if self.statut == "en-vol":
            self.statut = "atterrissage"

    def deplacer(self, delta_t_ms: int):
        if self.statut in ("crash", "atterri"):
            return

        distance = self.vitesse / 2000.0

        angle_rad = math.radians(90 - self.cap)
        self.x += distance * math.cos(angle_rad)
        self.y += distance * math.sin(angle_rad)

        if self.statut == "atterrissage" and self.altitude > 0:
            self.altitude = max(0, self.altitude - 100)

