from fruit_manager import ouvrir_inventaire
from geolocalisation import definir_geolocalisation, terre_ferme
from fruit import lire_fruits, creer_fruits
import random
import os
import json
import datetime
from typing import Dict, Any
import math

PLANTATIONS_PATH = "data/plantations.json"
SUPERFICIE_PLANTATION_MIN = 500    #en m^2
SUPERFICIE_PLANTATION_MAX = 25000    #en m^2
DISTANCE_MINIMUM_KM = 2.0  # Distance minimale entre deux plantations (en km)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcule la distance en kilomètres entre deux points géographiques en utilisant la formule de Haversine.
    
    Args:
        lat1, lon1: Latitude et longitude du premier point (en degrés)
        lat2, lon2: Latitude et longitude du second point (en degrés)
    
    Returns:
        float: Distance en kilomètres
    """
    # Rayon de la Terre en kilomètres
    R = 6371.0
    
    # Conversion des degrés en radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Différences de coordonnées
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Formule de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance en kilomètres
    distance = R * c
    return distance


def creer_plantation(lat: float = 40.8214, lon: float = 14.4265) -> Dict[str, Any]:
    """
    Crée une plantation avec géolocalisation, climat, répartition aléatoire des fruits
    et sauvegarde automatiquement dans le fichier JSON.

    Args:
        lat (float): Latitude de la plantation (ex: 40.8214)
        lon (float): Longitude de la plantation (ex: 14.4265)

    Returns:
        Dict[str, Any]: Dictionnaire représentant la plantation créée, comprenant :
            - 'geoloc': dict avec 'lat', 'lon' et 'climat'
            - 'climat': climat déterminé automatiquement à partir de la géolocalisation
            - 'superficie_totale': superficie totale de la plantation (float)
            - 'fruits_plantés': dictionnaire des fruits choisis et leur superficie
            - 'date_creation': date et heure de création (ISO string)
    """
    # Vérificarion qu'on est bien sur la terre ferme!
    if not terre_ferme(lat, lon):
        message = "Nous ne faisons pas d'élévage de crevettes et de moules! Veuillez choisir des coordonnées sur la terre ferme!"
        return {}, message
    
    # Vérifier la distance avec les plantations existantes
    plantations_existantes = lire_plantations()
    for plantation in plantations_existantes:
        existing_lat = plantation["geoloc"]["lat"]
        existing_lon = plantation["geoloc"]["lon"]
        distance = haversine_distance(lat, lon, existing_lat, existing_lon)
        if distance < DISTANCE_MINIMUM_KM:
            message = f"Impossible de créer la plantation car une autre plantation existe à {distance:.2f} km (distance minimale requise : {DISTANCE_MINIMUM_KM} km)."
            return {}, message
        
    geoloc = definir_geolocalisation(lat=lat, lon=lon)
    climat = geoloc["climat"]

    liste_fruits = lire_fruits()

    fruits_compatibles = [
        fruit for fruit in liste_fruits if climat in fruit.get("regions", [])
    ]

    
    superficie_totale = round(random.uniform(SUPERFICIE_PLANTATION_MIN, SUPERFICIE_PLANTATION_MAX), 2)
    
    k = random.randint(1, len(fruits_compatibles))
    varietes_selectionnes = random.sample(fruits_compatibles, k=k)

    proportions = [random.random() for _ in range(k)]
    total_proportion = sum(proportions)
    repartition_superficie = {
        fruit["nom"]: int(superficie_totale * (p / total_proportion))
        for fruit, p in zip(varietes_selectionnes, proportions)
    }

    fruits_plantes = {
        fruit["nom"]: {
            "superficie [m\u00B2]": repartition_superficie[fruit["nom"]],
        }
        for fruit in varietes_selectionnes
    }

    plantation = {
        "geoloc": geoloc,
        "climat": climat,
        "superficie_totale [m\u00B2]": superficie_totale,
        "fruits_plantés": fruits_plantes,
        "date_creation": datetime.datetime.now().isoformat()
    }

    os.makedirs(os.path.dirname(PLANTATIONS_PATH), exist_ok=True)
    plantations_existantes = []
    if os.path.exists(PLANTATIONS_PATH):
        with open(PLANTATIONS_PATH, "r", encoding="utf-8") as f:
            try:
                plantations_existantes = json.load(f)
            except:
                plantations_existantes = []

    plantations_existantes.append(plantation)

    with open(PLANTATIONS_PATH, "w", encoding="utf-8") as fichier:
        json.dump(plantations_existantes, fichier, ensure_ascii=False, indent=4)
        message = f"Nouvelle plantation crée aux coordonnées {lat}° N, {lon}° E"
    return plantation, message



def lire_plantations():
    """
    Lit toutes les plantations sauvegardées dans le fichier JSON.
    
    Returns:
        List[Dict[str, Any]]: Liste des plantations existantes. Chaque plantation
        est un dictionnaire structuré comme suit :
            - 'geoloc': dict avec
                - 'lat': latitude (float)
                - 'lon': longitude (float)
                - 'climat': climat déterminé automatiquement (str)
            - 'climat': climat de la plantation (str)
            - 'superficie_totale': superficie totale de la plantation en m² (float)
            - 'fruits_plantés': dictionnaire des fruits choisis, où chaque clé est
              le nom du fruit et la valeur un dictionnaire contenant :
                - 'superficie': superficie occupée par ce fruit (float)
                - 'specs': dictionnaire complet du fruit avec ses caractéristiques
            - 'date_creation': date et heure de création de la plantation (ISO string)
    """
    if os.path.exists(PLANTATIONS_PATH):
        with open(PLANTATIONS_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []


if __name__ == "__main__":
    creer_fruits()
    print(" -- Test1: plantation existante -- ")
    print("=================================")
    for i in range(2):
        plantation_test1, message1 = creer_plantation(20, 20)
    print(message1, end="\n\n") 
    
    print(" -- Test2: plantation sur l'eau -- ")
    print("===================================")
    plantation_test2, message2 = creer_plantation(0, -30)
    print(message2, end="\n\n")
    
    print(" -- Test3: plantation sur terre ferme et terrain vierge -- ")
    print("===========================================================")
    coords_existantes = [(p["geoloc"]["lat"], p["geoloc"]["lon"]) for p in lire_plantations()]
    while True:
        lat3 = random.uniform(-85, 85)
        lon3 = random.uniform(-180, 180)
        if all(abs(lat3 - lat) > 1 and abs(lon3 - lon) > 1 for lat, lon in coords_existantes):
            if terre_ferme(lat3, lon3):
                break
    plantation_test3, message3 = creer_plantation(lat3, lon3)
    print(message3)
    for key, value in plantation_test3.items():
        print(key)
        print("-"*len(key))
        print(value, "\n")