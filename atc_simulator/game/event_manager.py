import random

def evenements_aleatoires(espace_aerien):
    if not espace_aerien.liste_avions:
        return []

    evenements = []

    for avion in espace_aerien.liste_avions:
        if random.random() < 0.1:
            type_evenement = random.choice(["panne", "météo", "détresse", "rien"])

            match type_evenement:
                case "panne":
                    if avion.statut == "en-vol":
                        avion.statut = "urgence"
                        evenements.append(f"Panne technique : {avion.id_vol} !")
                case "météo":
                    evenements.append(f"Conditions météo difficiles pour {avion.id_vol}.")
                case "détresse":
                    avion.statut = "détresse"
                    evenements.append(f"{avion.id_vol} en détresse !")
                case "rien" | _:
                    continue
    return evenements