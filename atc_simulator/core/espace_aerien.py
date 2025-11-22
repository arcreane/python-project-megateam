import random
import math
from .avion import Avion
class EspaceAerien:

    def __init__(self, radar_range_km):
        self.liste_avions = []
        self.radar_range_km = radar_range_km
        self.zone_atterrissage = (radar_range_km / 2, 10, 10, 10)  # (x, y, z, h)
        self.collisions_detectees = 0
        self.atterrissages_reussis = 0

    def ajouter_avion(self):
        lettre = random.choice(['AF','LH','MC','AN'])
        code = random.randint(100,999)
        id_vol = f"{lettre}{code}"
        x = random.choice([0, self.radar_range_km])
        y = random.uniform(20, self.radar_range_km - 20)
        avion = Avion(id_vol, x, y, 8, 400, 180)
        self.liste_avions.append(avion)

    def update_positions(self, delta_t_ms):
        for avion in self.liste_avions:
            avion.deplacer(delta_t_ms)

    def detecter_collisions(self):
        for i in range(len(self.liste_avions)):
            for j in range(i + 1, len(self.liste_avions)):
                avion1 = self.liste_avions[i]
                avion2 = self.liste_avions[j]
                dist_horiz = math.sqrt((avion1.x - avion2.x) ** 2 + (avion1.y - avion2.y) ** 2)
                dist_vert = abs(avion1.altitude - avion2.altitude)

                if dist_horiz < 5 and dist_vert < 0.3 :
                    # 5km est le seuil de distance de danger horizontal
                    # 0.3km est le seuil de distance de danger vertical
                    avion1.statut = "crash"
                    avion2.statut = "crash"
                    self.collisions_detectees += 1
                    return True
        return False

    def dans_zone_atterrissage(self, avion):
        x, y, z, h = self.zone_atterrissage
        return (x <= avion.x <= x + z) and (y <= avion.y <= y + h)

    def gerer_atterrissages(self):
        atterrissage_reussi = False

        for avion in self.liste_avions:
            condition_altitude = (avion.altitude < 0.1)
            if self.dans_zone_atterrissage(avion) and avion.statut == "atterrissage" and condition_altitude:
                avion.statut = "atterri"
                self.atterrissages_reussis += 1
                atterrissage_reussi = True

        return atterrissage_reussi
