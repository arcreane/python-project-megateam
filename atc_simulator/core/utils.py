import json
import datetime

def charger_config(fichier_json):
    try:
        with open(fichier_json, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"ERREUR: Fichier config '{fichier_json}' non trouvé.")
        return None
    except json.JSONDecodeError:
        print(f"ERREUR: Fichier '{fichier_json}' est mal formaté.")
        return None

def log_action(action_type, *args, **kwargs):
    log_entry = f"[{action_type.upper()}]"
    if args:
        log_entry += f" Params: {args}"
    if kwargs:
        log_entry += f" Détails: {kwargs}"
    print(log_entry)

