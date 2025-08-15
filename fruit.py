import json
import os

DATA_DIR = "data"
FRUITS_PATH = os.path.join(DATA_DIR, "fruits.json")

fruits_defaut = [
    {
        "nom": "bananes",
        "icone": "🍌",
        "semis_debut": "03-01",
        "semis_fin": "04-15",
        "recolte_debut": "09-01",
        "recolte_fin": "10-15",
        "rendement_m2": 5,
        "cout_exploitation_unitaire": 0.20,
        "prix_vente_unitaire": 2.00,
        "regions": ["tropical", "subtropical"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.8,
            "vent_fort": 0.85,
            "sécheresse": 0.7,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    },
    {
        "nom": "mangues",
        "icone": "🥭",
        "semis_debut": "02-15",
        "semis_fin": "03-30",
        "recolte_debut": "07-15",
        "recolte_fin": "08-30",
        "rendement_m2": 3,
        "cout_exploitation_unitaire": 0.50,
        "prix_vente_unitaire": 7.00,
        "regions": ["tropical", "subtropical"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.8,
            "sécheresse": 0.6,
            "gel": 0.5,
            "chaleur_extrême": 0.7
        }
    },
    {
        "nom": "ananas",
        "icone": "🍍",
        "semis_debut": "01-01",
        "semis_fin": "01-31",
        "recolte_debut": "06-01",
        "recolte_fin": "06-30",
        "rendement_m2": 4,
        "cout_exploitation_unitaire": 0.40,
        "prix_vente_unitaire": 5.00,
        "regions": ["tropical", "subtropical"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.8,
            "sécheresse": 0.6,
            "gel": 0.5,
            "chaleur_extrême": 0.7
        }
    },
    {
        "nom": "noix de coco",
        "icone": "🥥",
        "semis_debut": "04-01",
        "semis_fin": "05-31",
        "recolte_debut": "11-01",
        "recolte_fin": "12-31",
        "rendement_m2": 2,
        "cout_exploitation_unitaire": 0.60,
        "prix_vente_unitaire": 4.00,
        "regions": ["tropical", "subtropical"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.8,
            "sécheresse": 0.6,
            "gel": 0.5,
            "chaleur_extrême": 0.7
        }
    },
    {
        "nom": "pastèques",
        "icone": "🍉",
        "semis_debut": "04-15",
        "semis_fin": "05-15",
        "recolte_debut": "08-01",
        "recolte_fin": "09-15",
        "rendement_m2": 1,
        "cout_exploitation_unitaire": 0.80,
        "prix_vente_unitaire": 3.50,
        "regions": ["tempéré", "méditerranéen"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.8,
            "vent_fort": 0.85,
            "sécheresse": 0.6,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    },
    {
        "nom": "avocats",
        "icone": "🥑",
        "semis_debut": "03-15",
        "semis_fin": "04-30",
        "recolte_debut": "10-01",
        "recolte_fin": "11-15",
        "rendement_m2": 2,
        "cout_exploitation_unitaire": 0.70,
        "prix_vente_unitaire": 5.00,
        "regions": ["subtropical", "méditerranéen"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.8,
            "sécheresse": 0.7,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    },
    {
        "nom": "pommes",
        "icone": "🍎",
        "semis_debut": "02-01",
        "semis_fin": "03-15",
        "recolte_debut": "09-01",
        "recolte_fin": "10-15",
        "rendement_m2": 4,
        "cout_exploitation_unitaire": 0.25,
        "prix_vente_unitaire": 2.50,
        "regions": ["tempéré"],
        "facteur_meteo": {
            "soleil_optimale": 1.1,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.9,
            "sécheresse": 0.8,
            "gel": 0.6,
            "chaleur_extrême": 0.7
        }
    },
    {
        "nom": "poires",
        "icone": "🍐",
        "semis_debut": "02-15",
        "semis_fin": "03-31",
        "recolte_debut": "09-15",
        "recolte_fin": "10-30",
        "rendement_m2": 4,
        "cout_exploitation_unitaire": 0.30,
        "prix_vente_unitaire": 2.80,
        "regions": ["tempéré"],
        "facteur_meteo": {
            "soleil_optimale": 1.1,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.9,
            "sécheresse": 0.8,
            "gel": 0.6,
            "chaleur_extrême": 0.7
        }
    },
    {
        "nom": "fraises",
        "icone": "🍓",
        "semis_debut": "03-01",
        "semis_fin": "04-15",
        "recolte_debut": "06-01",
        "recolte_fin": "07-15",
        "rendement_m2": 10,
        "cout_exploitation_unitaire": 0.15,
        "prix_vente_unitaire": 1.50,
        "regions": ["tempéré", "méditerranéen"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.85,
            "sécheresse": 0.7,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    },
    {
        "nom": "cerises",
        "icone": "🍒",
        "semis_debut": "02-15",
        "semis_fin": "03-15",
        "recolte_debut": "06-15",
        "recolte_fin": "07-10",
        "rendement_m2": 5,
        "cout_exploitation_unitaire": 0.35,
        "prix_vente_unitaire": 4.00,
        "regions": ["tempéré"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.85,
            "sécheresse": 0.7,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    },
    {
        "nom": "raisins",
        "icone": "🍇",
        "semis_debut": "03-01",
        "semis_fin": "04-10",
        "recolte_debut": "09-10",
        "recolte_fin": "10-05",
        "rendement_m2": 6,
        "cout_exploitation_unitaire": 0.40,
        "prix_vente_unitaire": 3.00,
        "regions": ["tempéré", "méditerranéen"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.85,
            "sécheresse": 0.7,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    },
    {
        "nom": "citron",
        "icone": "🍋",
        "semis_debut": "03-10",
        "semis_fin": "04-30",
        "recolte_debut": "11-15",
        "recolte_fin": "12-31",
        "rendement_m2": 3,
        "cout_exploitation_unitaire": 0.25,
        "prix_vente_unitaire": 2.20,
        "regions": ["méditerranéen"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.85,
            "sécheresse": 0.7,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    },
    {
        "nom": "prunes",
        "icone": "🍑",
        "semis_debut": "02-15",
        "semis_fin": "03-20",
        "recolte_debut": "08-10",
        "recolte_fin": "09-05",
        "rendement_m2": 4,
        "cout_exploitation_unitaire": 0.28,
        "prix_vente_unitaire": 3.00,
        "regions": ["tempéré"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.85,
            "sécheresse": 0.7,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    },
    {
        "nom": "figues",
        "icone": "🍈",
        "semis_debut": "03-05",
        "semis_fin": "04-10",
        "recolte_debut": "08-20",
        "recolte_fin": "09-25",
        "rendement_m2": 2,
        "cout_exploitation_unitaire": 0.45,
        "prix_vente_unitaire": 4.50,
        "regions": ["méditerranéen"],
        "facteur_meteo": {
            "soleil_optimale": 1.2,
            "ensoleillé": 1.0,
            "nuageux": 0.9,
            "pluie_moderée": 1.0,
            "pluie_forte": 0.85,
            "vent_fort": 0.85,
            "sécheresse": 0.7,
            "gel": 0.5,
            "chaleur_extrême": 0.6
        }
    }
]


def creer_fruits(path=FRUITS_PATH, list_fruits = fruits_defaut):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
       
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(list_fruits, f, ensure_ascii=False, indent=4)
        print(f"Fichier {path} créé avec les fruits par défaut.")
    else:
        print(f"Fichier {path} existe déjà.")
        
        
    
def lire_fruits(path=FRUITS_PATH):
    if os.path.exists(path):
       
        with open(path, 'r', encoding='utf-8') as fichier:
            try:
                return json.load(fichier)
            except:
                return []
    return []
        
        
        
        
if __name__ == "__main__":
    creer_fruits()
