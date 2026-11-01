import json
import sqlite3
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "plantation.db"

def connexion():
    DATA_DIR.mkdir(exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    return con

def creer_tables():
    with connexion() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS fruits (
            nom    TEXT PRIMARY KEY,
            prix   REAL NOT NULL CHECK (prix > 0),
            stock  INTEGER NOT NULL CHECK (stock >= 0)
        );
        CREATE TABLE IF NOT EXISTS clients (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nom  TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS ventes (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            date       TEXT NOT NULL,
            client_id  INTEGER REFERENCES clients(id),
            fruit      TEXT NOT NULL REFERENCES fruits(nom),
            quantite   INTEGER NOT NULL CHECK (quantite > 0),
            montant    REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tresorerie (
            date   TEXT NOT NULL,
            solde  REAL NOT NULL
        );
        """)
        
def importer_json():
    with connexion() as con:
        if con.execute("SELECT COUNT(*) FROM fruits").fetchone()[0] > 0:
            print("Base déjà remplie : import ignoré.")
            return

        prix = json.loads((DATA_DIR / "prix.json").read_text(encoding="utf-8"))
        stock = json.loads((DATA_DIR / "inventaire.json").read_text(encoding="utf-8"))
        con.executemany(
            "INSERT INTO fruits (nom, prix, stock) VALUES (?, ?, ?)",
            [(fruit, prix[fruit], stock.get(fruit, 0)) for fruit in prix],
        )

        fichier_histo = DATA_DIR / "tresorerie_history.json"
        if fichier_histo.exists():
            historique = json.loads(fichier_histo.read_text(encoding="utf-8"))
            con.executemany(
                "INSERT INTO tresorerie (date, solde) VALUES (?, ?)",
                [(ligne["timestamp"], ligne["tresorerie"]) for ligne in historique],
            )
        else:
            solde = json.loads((DATA_DIR / "tresorerie.txt").read_text(encoding="utf-8"))
            con.execute(
                "INSERT INTO tresorerie (date, solde) VALUES (?, ?)",
                (datetime.now().isoformat(timespec="seconds"), solde),
            )
        print(f"Importé : {len(prix)} fruits.")


def lire_inventaire():
    with connexion() as con:
        return dict(con.execute("SELECT nom, stock FROM fruits ORDER BY nom"))

def lire_prix():
    with connexion() as con:
        return dict(con.execute("SELECT nom, prix FROM fruits ORDER BY nom"))
    
def lire_tresorerie():
    with connexion() as con:
        ligne = con.execute("SELECT solde FROM tresorerie ORDER BY rowid DESC LIMIT 1").fetchone()
        return ligne[0]

def lire_historique():
    with connexion() as con:
        lignes = con.execute("SELECT date, solde FROM tresorerie ORDER BY rowid")
        return [{"timestamp": date, "tresorerie": solde} for date, solde in lignes]

def maintenant():
    return datetime.now().isoformat(timespec="seconds")

def recolter(fruit, quantite):
    if quantite <= 0:
        return {"status": "error", "text": "La quantité doit être positive."}
    with connexion() as con:
        con.execute("UPDATE fruits SET stock = stock + ? WHERE nom = ?", (quantite, fruit))
    return {"status": "success", "text": f"Récolté {quantite} {fruit} supplémentaires !"}

def vendre(fruit, quantite, client=""):
    if quantite <= 0:
        return {"status": "error", "text": "La quantité doit être positive."}
    with connexion() as con:
        stock, prix = con.execute(
            "SELECT stock, prix FROM fruits WHERE nom = ?", (fruit,)
        ).fetchone()
        if stock < quantite:
            return {"status": "error", "text": f"Pas assez de {fruit} : il en reste {stock}."}

        client_id = None
        if client.strip():
            con.execute("INSERT OR IGNORE INTO clients (nom) VALUES (?)", (client.strip(),))
            client_id = con.execute(
                "SELECT id FROM clients WHERE nom = ?", (client.strip(),)
            ).fetchone()[0]

        montant = prix * quantite
        solde = con.execute(
            "SELECT solde FROM tresorerie ORDER BY rowid DESC LIMIT 1"
        ).fetchone()[0]

        con.execute("UPDATE fruits SET stock = stock - ? WHERE nom = ?", (quantite, fruit))
        con.execute(
            "INSERT INTO ventes (date, client_id, fruit, quantite, montant) VALUES (?, ?, ?, ?, ?)",
            (maintenant(), client_id, fruit, quantite, montant),
        )
        con.execute(
            "INSERT INTO tresorerie (date, solde) VALUES (?, ?)",
            (maintenant(), solde + montant),
        )
    return {"status": "success", "text": f"Vendu {quantite} {fruit} pour {montant:.2f} $."}



    
if __name__ == "__main__":
    creer_tables()
    importer_json()
    with connexion() as con:
        for ligne in con.execute("SELECT * FROM fruits"):
            print(ligne)


