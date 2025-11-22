class ScoreManager:
    SCORE_ATTERRISSAGE = 100
    PENALITE_COLLISION = -50

    def __init__(self):
        self.score_actuel = 0



    def reset_score(self):
        self.score_actuel = 0



    def evenement_jeu(self, type_evenement):
        if type_evenement == "atterrissage":
            self.score_actuel += self.SCORE_ATTERRISSAGE
        elif type_evenement == "collision":
            self.score_actuel += self.PENALITE_COLLISION