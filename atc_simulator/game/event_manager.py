import random

def generer_evenement_aleatoire(espace_aerien):
    if not espace_aerien.liste_avions or random.randint(0, 200) != 42:
        return None

    type_evenement = random.choice(["panne", "rien"])
    avion_concerne = random.choice(espace_aerien.liste_avions)

    match type_evenement:
        case "panne":
            if avion_concerne.statut == "en-vol":
                avion_concerne.statut = "urgence"
                return f"Panne technique: {avion_concerne.id_vol}!"
        case "rien" | _:
            return None