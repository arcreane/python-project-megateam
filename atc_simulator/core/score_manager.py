class ScoreManager:
    def __init__(self):
        self.score = 0

    def reset(self):
        self.score = 0

    def appliquer_evenement(self, type_evenement: str):
        if type_evenement == "atterrissage":
            self.score += 100
        elif type_evenement == "collision":
            self.score -= 50
