
from typing import Dict, List
import requests

REGIONS_CLIMATS = {
    "tropical": "Chaud et humide toute l’année",
    "subtropical": "Chaud, hiver doux, pluies saisonnières",
    "tempéré": "Saisons distinctes, été chaud, hiver froid",
    "méditerranéen": "Été chaud et sec, hiver doux et humide",
    "froid": "Zone froide au nord"
}


def definir_geolocalisation(lat: float = 40.8214, lon: float = 14.4265) -> Dict[str, float] :
    """
    Définir la position de la plantation.
    Par défaut : le Vésuve (Italie), idéeal pour planter les tomates!
    lat : latitude
    lon : longitude
    """
    
    abs_lat = abs(lat)
    # Définition symétrique des climats
    if 0 <= abs_lat <= 23:
        climat = "tropical"
    elif 23 < abs_lat <= 30:
        climat = "subtropical"
    elif 30 < abs_lat <= 45:
        climat = "méditerranéen"
    elif 45 < abs_lat <= 66:
        climat = "tempéré"
    else:
        climat = "froid"
    
    return {
        "lat": lat,
        "lon": lon,
        "climat": climat
    }
    
    


def terre_ferme(lat: float, lon: float) -> bool:
    url = f"https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": lat,
        "lon": lon,
        "zoom": 10,
        "addressdetails": 1
    }
    headers = {"User-Agent": "plantation-script"}
    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    return "country" in data.get("address", {})


if __name__ == "__main__":
    print("Paris: ", definir_geolocalisation(48.8566, 2.3522))   
    print("Équateur: ", definir_geolocalisation(0, 0))             
    print("Australie: ", definir_geolocalisation(-36.0, 147.0))      
    print("Test1, est sur la terre ferme: ", terre_ferme(48.8566, 2.3522))  # True
    print("Test2, n'est sur la terre ferme: ",terre_ferme(0, -30))  # False
