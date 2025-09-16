# 🍇 Fruit Manager

Bienvenue sur **Fruit Manager**, un tableau de bord interactif pour gérer votre plantation de fruits ! Ce projet, développé avec Streamlit, vous permet de suivre votre inventaire, vendre et récolter des fruits, et surveiller votre trésorerie en temps réel.

## 🛠️ Installation

### Option 1 — Local avec Poetry

Création de l'environnement virtuel :
```bash
poetry install
```

Lancez le projet avec poetry :
```bash
poetry run streamlit run app.py
```
### Option 2 — Avec Docker

Construire l’image :
```bash
docker build -t fruit-manager .
```

Lancer le container :
```bash
docker run -p 8501:8501 fruit-manager
```
ou bien directement depuis Docker Desktop :<br>
Images -> Run image (logo triangle) -> Optional settings (ajouter un nom de container et le port 8501).

💡 Note dev : Pour bénéficier de l’autocomplétion et du confort de l’IDE, il est conseillé d’installer aussi les dépendances en local (via Poetry).<br>
Docker utilise un requirements.txt minimal pour l’exécution.

## 🚀 Fonctionnalités

- **Vente de fruits** : Sélectionnez un fruit, indiquez la quantité à vendre et mettez à jour votre trésorerie automatiquement.
- **Récolte** : Ajoutez facilement de nouveaux fruits à votre inventaire après chaque récolte.
- **Suivi de la trésorerie** : Visualisez le montant disponible après chaque opération.

## 📁 Structure du projet

- `app.py` : Interface principale Streamlit.
- `fruit_manager.py` : Fonctions de gestion de l'inventaire, des ventes, des récoltes et de la trésorerie.
- `data/` : Fichiers de données (inventaire, prix du marché, trésorerie).
- `requirements.txt` : Dépendances minimales pour exécuter le projet avec Docker.

## ✨ Exemple d'utilisation

- Accédez à l'interface web générée par Streamlit.
- Utilisez la barre latérale pour vendre ou récolter des fruits.
- Consultez l'inventaire et la trésorerie mis à jour en temps réel.

## 🤝 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request pour proposer des améliorations.


---

**Bonnes récoltes et bonnes ventes !** 🍏🍒🍊