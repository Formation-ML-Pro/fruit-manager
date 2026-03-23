import json
import os
import datetime
import uuid

DATA_DIR = "data"
PRIX_PATH = os.path.join(DATA_DIR, "prix.json")
INVENTAIRE_PATH = os.path.join(DATA_DIR, "inventaire.json")
TRESORERIE_PATH = os.path.join(DATA_DIR, "tresorerie.txt")
COMMANDES_PATH = os.path.join(DATA_DIR, "commandes.json")


def enregistrer_tresorerie_historique(
    tresorerie, fichier="data/tresorerie_history.json"
):
    historique = []
    if os.path.exists(fichier):
        with open(fichier, "r") as f:
            try:
                historique = json.load(f)
            except:
                historique = []
    historique.append(
        {"timestamp": datetime.datetime.now().isoformat(), "tresorerie": tresorerie}
    )
    with open(fichier, "w") as f:
        json.dump(historique, f)


def lire_tresorerie_historique(fichier="data/tresorerie_history.json"):
    if os.path.exists(fichier):
        with open(fichier, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []


def ouvrir_prix(path=PRIX_PATH):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        prix_defaut = {
            "bananes": 2,
            "mangues": 7,
            "ananas": 5,
            "noix de coco": 4,
            "papayes": 3,
        }
        with open(path, "w", encoding="utf-8") as fichier:
            json.dump(prix_defaut, fichier, ensure_ascii=False, indent=4)
    with open(path, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def ouvrir_inventaire(path=INVENTAIRE_PATH):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        inventaire_defaut = {
            "bananes": 120,
            "mangues": 85,
            "ananas": 45,
            "noix de coco": 60,
            "papayes": 30,
        }
        with open(path, "w", encoding="utf-8") as fichier:
            json.dump(inventaire_defaut, fichier, ensure_ascii=False, indent=4)
    with open(path, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def ecrire_inventaire(inventaire, path="data/inventaire.json"):
    with open(path, "w", encoding="utf-8") as fichier:
        json.dump(inventaire, fichier, ensure_ascii=False, indent=4)


def ouvrir_tresorerie(path=TRESORERIE_PATH):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fichier:
            json.dump(1000.0, fichier)
    with open(path, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def ecrire_tresorerie(tresorerie, path="data/tresorerie.txt"):
    with open(path, "w", encoding="utf-8") as fichier:
        json.dump(tresorerie, fichier, ensure_ascii=False, indent=4)


def afficher_tresorerie(tresorerie):
    print(f"\n💰 Trésorerie actuelle : {tresorerie:.2f} $")


def afficher_inventaire(inventaire):
    print("Inventaire actuel de la plantation :")
    for fruit, quantite in inventaire.items():
        print(f"- {fruit.capitalize()} : {quantite} unités")


def recolter(inventaire, fruit, quantite):
    inventaire[fruit] = inventaire.get(fruit, 0) + quantite
    message = {
        "status": "success",
        "text": f"\nRécolté {quantite} {fruit} supplémentaires !",
    }
    return (inventaire, message)


def vendre(inventaire, fruit, quantite, tresorerie, prix):
    if inventaire.get(fruit, 0) >= quantite:
        inventaire[fruit] -= quantite
        tresorerie += prix.get(fruit, 0) * quantite
        enregistrer_tresorerie_historique(tresorerie)
        message = {"status": "success", "text": f"\nVendu {quantite} {fruit} !"}
        return (inventaire, tresorerie, message)
    else:
        message = {
            "status": "error",
            "text": f"\nPas assez de {fruit} pour en vendre {quantite}.",
        }
        return (inventaire, tresorerie, message)


def vendre_tout(inventaire, tresorerie, prix):
    print("\n🛒 Vente de tout l'inventaire :")
    for fruit, quantite in list(inventaire.items()):
        if quantite > 0:
            revenu = prix.get(fruit, 0) * quantite
            tresorerie += revenu
            print(
                f"- {fruit.capitalize()} : vendu {quantite} unités pour {revenu:.2f} $"
            )
            inventaire[fruit] = 0
    return inventaire, tresorerie


def valeur_stock(inventaire, prix):
    valeur = {}
    for fruit in inventaire:
        quantite = inventaire[fruit]
        prix_unitaire = prix.get(fruit, 0)
        valeur[fruit] = quantite * prix_unitaire
    return valeur


def dollar_to_euro(tresorerie):
    taux_de_change = 0.86
    tresorerie_euro = tresorerie * taux_de_change
    return tresorerie_euro


# --- Fonction de gestion des commandes clients ---
def lire_commandes(path=COMMANDES_PATH):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


def ecrire_commandes(commandes, path=COMMANDES_PATH):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(commandes, f, ensure_ascii=False, indent=4)


def passer_commande(nom_client, adresse, telephone, panier, prix):
    total = sum(panier.get(fruit, 0) * prix.get(fruit, 0) for fruit in panier)
    commande = {
        "id": str(uuid.uuid4())[:8].upper(),
        "timestamp": datetime.datetime.now().isoformat(),
        "client": nom_client,
        "adresse": adresse,
        "telephone": telephone,
        "panier": panier,
        "total": total,
        "statut": "en_attente",
    }
    commandes = lire_commandes()
    commandes.append(commande)
    ecrire_commandes(commandes)
    return commande


def valider_commande(commande_id, inventaire, tresorerie, prix):
    commandes = lire_commandes()
    for commande in commandes:
        if commande["id"] == commande_id and commande["statut"] == "en_attente":
            for fruit, qte in commande["panier"].items():
                if inventaire.get(fruit, 0) < qte:
                    return inventaire, tresorerie, {
                        "status": "error",
                        "text": f"Stock insuffisant pour {fruit} (dispo: {inventaire.get(fruit, 0)}, demandé: {qte})",
                    }
            for fruit, qte in commande["panier"].items():
                inventaire[fruit] -= qte
            tresorerie += commande["total"]
            enregistrer_tresorerie_historique(tresorerie)
            commande["statut"] = "validée"
            ecrire_commandes(commandes)
            return inventaire, tresorerie, {
                "status": "success",
                "text": f"Commande #{commande_id} validée ! +{commande['total']:.2f} $",
            }
    return inventaire, tresorerie, {"status": "error", "text": "Commande introuvable."}


def annuler_commande(commande_id):
    commandes = lire_commandes()
    for commande in commandes:
        if commande["id"] == commande_id and commande["statut"] == "en_attente":
            commande["statut"] = "annulée"
            ecrire_commandes(commandes)
            return {"status": "success", "text": f"Commande #{commande_id} annulée."}
    return {"status": "error", "text": "Commande introuvable ou déjà traitée."}


if __name__ == "__main__":
    inventaire = ouvrir_inventaire()
    tresorerie = ouvrir_tresorerie()
    prix = ouvrir_prix()
    afficher_tresorerie(tresorerie)
    afficher_inventaire(inventaire)

    recolter(inventaire, "bananes", 10)
    vendre(inventaire, "bananes", 5, tresorerie, prix)
    #inventaire, tresorerie = vendre(inventaire, "bananes", 5, tresorerie, prix)

    ecrire_inventaire(inventaire)
    ecrire_tresorerie(tresorerie)
