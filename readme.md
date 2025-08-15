# 🍇 Fruit Manager

Bienvenue sur **Fruit Manager**, un tableau de bord interactif pour gérer votre plantation de fruits ! Ce projet, développé avec Streamlit, vous permet de suivre votre inventaire, vendre et récolter des fruits, et surveiller votre trésorerie en temps réel.

## 🛠️ Installation

Création de l'environnement virtuel :
```bash
poetry install
```

Lancez le projet avec poetry :
```bash
poetry run streamlit run app.py
```

## 🚀 Fonctionnalités

- **Vente de fruits** : Sélectionnez un fruit, indiquez la quantité à vendre et mettez à jour votre trésorerie automatiquement.
- **Récolte** : Ajoutez facilement de nouveaux fruits à votre inventaire après chaque récolte.
- **Suivi de la trésorerie** : Visualisez le montant disponible après chaque opération.
- **Géolocalisation et climat** : Déterminez automatiquement le climat (tropical, subtropical, méditerranéen, tempéré, froid) en fonction de la latitude et de la longitude.
- **Gestion des plantations** : Créez et gérez des plantations avec une géolocalisation précise, un climat déterminé automatiquement et une répartition aléatoire des fruits adaptés au climat.
- **Catalogue de fruits** : Gérez une liste de fruits avec leurs caractéristiques (périodes de semis et récolte, rendement, coûts, prix de vente, compatibilité climatique).

## 📁 Structure du projet

- `app.py` : Interface principale Streamlit.
- `fruit_manager.py` : Fonctions de gestion de l'inventaire, des ventes, des récoltes et de la trésorerie.
- `data/` : Fichiers de données (inventaire, prix du marché, trésorerie).
- `geolocalisation.py` : Détermine le climat d'une plantation en fonction de sa latitude et longitude.
- `fruit.py` : Gère le catalogue des fruits et leurs caractéristiques (rendement, coûts, météo).
- `plantation.py` : Crée et gère les plantations avec géolocalisation, superficie et répartition des fruits.
- `data/` : Fichiers de données (inventaire, prix du marché, trésorerie).
  - `fruits.json` : Catalogue des fruits avec leurs caractéristiques.
  - `plantations.json` : Données des plantations créées (géolocalisation, fruits plantés, superficie).



## ✨ Exemple d'utilisation

- Accédez à l'interface web générée par Streamlit.
- Utilisez la barre latérale pour vendre ou récolter des fruits.
- Consultez l'inventaire et la trésorerie mis à jour en temps réel.

## 🤝 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request pour proposer des améliorations.


---

**Bonnes récoltes et bonnes ventes !** 🍏🍒🍊