import random

class EspaceAerien:
    def __init__(self, radar_range_km):
        self.liste_avions = []
        self.radar_range_km = radar_range_km
        self.zone_atterrissage = (radar_range_km / 2 - 5, 10, 10, 5)  # (x, y, w, h)
        self.collisions_detectees = 0
        self.atterrissages_reussis = 0

    def ajouter_avion(self):
        id_vol = f"AF{random.randint(100, 999)}"
        x = random.choice([0, self.radar_range_km])
        y = random.uniform(20, self.radar_range_km - 20)
        avion = Avion(id_vol, x, y, 8000, 400, 180)
        self.liste_avions.append(avion)

    def update_positions(self, tick_duration_ms):
        for avion in self.liste_avions:
            avion.deplacer(tick_duration_ms)
