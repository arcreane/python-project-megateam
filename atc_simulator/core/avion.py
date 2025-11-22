class Avion:
   import math
    def __init__(self, id_vol, x, y, altitude, vitesse, cap, carburant=100):
        self.id_vol = id_vol
        self.x = x
        self.y = y
        self.altitude = altitude
        self.vitesse = vitesse
        self.cap = cap
        self.carburant = carburant

    def __del__(self):
        print(f"Destructeur: Avion {self.id_vol} retiré.")

    def changer_altitude(self, altitude_cible):
        if altitude_cible < 500 and self.statut != "atterrissage":
            raise AltitudeError(f"Ordre dangereux pour {self.id_vol}: {altitude_cible}m.")
        self.altitude = altitude_cible

    def changer_cap(self, cap_cible):
        self.cap = cap_cible % 360

    def deplacer(self, tick_duration_ms):
        if self.statut == "atterrissage" and self.altitude < 500:
            self.altitude = max(0, self.altitude - 20)
            if self.altitude == 0:
                self.statut = "atterri"
            return

        temps_h = tick_duration_ms / (1000 * 60 * 60)
        distance = self.vitesse * temps_h
        angle_rad = math.radians(90 - self.cap)

        self.x += distance * math.cos(angle_rad)
        self.y += distance * math.sin(angle_rad)

