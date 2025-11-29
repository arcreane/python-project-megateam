import random
import math
import random
import math
from avion import Avion


class EspaceAerien:
    def __init__(self, taille: float):
        self.taille = taille
        self.liste_avions = []
        self.zone_atterrissage = (taille / 2 - 5, 5, 10, 10)
        self.collisions_detectees = 0
        self.atterrissages_reussis = 0


    def ajouter_avion(self):
        prefixes = ["AF", "MC", "LH", "AN"]
        code = random.randint(100, 999)
        id_vol = f"{random.choice(prefixes)}{code}"

        x = random.choice([0, self.taille])
        y = random.uniform(self.taille * 0.3, self.taille * 0.9)
        altitude = random.randint(2000, 8000)
        vitesse = random.randint(300, 600)

        cap = 90 if x == 0 else 270

        avion = Avion(id_vol, x, y, altitude, vitesse, cap)
        self.liste_avions.append(avion)

    def mettre_a_jour(self, delta_t_ms: int):
        for avion in self.liste_avions:
            avion.deplacer(delta_t_ms)

    def _avions_actifs(self):
        return [a for a in self.liste_avions if a.statut not in ("crash", "atterri")]

    def detecter_collisions(self) -> bool:
        collision = False
        actifs = self._avions_actifs()

        for i in range(len(actifs)):
            for j in range(i + 1, len(actifs)):
                a1 = actifs[i]
                a2 = actifs[j]
                dist_h = math.sqrt((a1.x - a2.x)**2 + (a1.y - a2.y)**2)
                dist_v = abs(a1.altitude - a2.altitude)

                if dist_h < 3 and dist_v < 300:
                    a1.statut = "crash"
                    a2.statut = "crash"
                    collision = True

        if collision:
            self.collisions_detectees += 1
        return collision

    def avion_dans_zone_atterrissage(self, avion: Avion) -> bool:
        x, y, w, h = self.zone_atterrissage
        return x <= avion.x <= x + w and y <= avion.y <= y + h

    def gerer_atterrissages(self):

        reussi = False
        crash_au_sol = False

        for avion in self.liste_avions:
            if avion.statut == "atterrissage" and avion.altitude == 0:
                if self.avion_dans_zone_atterrissage(avion):
                    avion.statut = "atterri"
                    self.atterrissages_reussis += 1
                    reussi = True
                else:
                    avion.statut = "crash"
                    self.collisions_detectees += 1
                    crash_au_sol = True

        return reussi, crash_au_sol

    def nettoyer_avions(self):
        self.liste_avions = [
            a for a in self.liste_avions
            if a.statut not in ("crash", "atterri")
        ]

    def get_avion_selectionne(self):
        for a in self.liste_avions:
            if a.selectionne:
                return a
        return None

    def selectionner_par_id(self, id_vol: str):
        selectionne = None
        for a in self.liste_avions:
            a.selectionne = (a.id_vol == id_vol)
            if a.selectionne:
                selectionne = a
        return selectionne
