import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from fruit_manager import ouvrir_inventaire, ouvrir_prix, passer_commande

st.title("🛒 Passer votre commande en ligne")
st.write("Bienvenue dans notre plantation ! Sélectionnez vos fruits.")

inventaire = ouvrir_inventaire()
prix = ouvrir_prix()

# --- Initialisation du panier en session ---
if "panier" not in st.session_state:
    st.session_state.panier = {}

# --- Catalogue des fruits disponibles ---
st.header("🍍 Nos fruits disponibles")

fruits_disponibles = {f: q for f, q in inventaire.items() if q > 0}

if not fruits_disponibles:
    st.warning("Aucun fruit disponible en stock pour le moment. Revenez bientôt !")
    st.stop()

cols = st.columns(len(fruits_disponibles))
EMOJIS = {"bananes": "🍌", "mangues": "🥭", "ananas": "🍍", "noix de coco": "🥥", "papayes": "🍈"}

for col, (fruit, stock) in zip(cols, fruits_disponibles.items()):
    with col:
        emoji = EMOJIS.get(fruit, "🍓")
        st.markdown(f"### {emoji} {fruit.capitalize()}")
        st.markdown(f"**Prix :** {prix.get(fruit, 0)} €/unité")
        st.markdown(f"*Stock : {stock} unités*")

        max_qte = min(stock, 50)
        qte = st.number_input(
            "Quantité",
            min_value=0,
            max_value=max_qte,
            step=1,
            key=f"qte_{fruit}",
        )
        if st.button("Ajouter au panier", key=f"add_{fruit}"):
            if qte > 0:
                st.session_state.panier[fruit] = st.session_state.panier.get(fruit, 0) + qte
                st.success(f"{qte} {fruit} ajouté(s) !")
            else:
                st.warning("Entrez une quantité supérieure à 0.")

# --- Affichage du panier ---
st.divider()
st.header("🧺 Mon panier")

if not st.session_state.panier:
    st.info("Votre panier est vide. Ajoutez des fruits.")
else:
    total = 0
    lignes = []
    for fruit, qte in list(st.session_state.panier.items()):
        prix_unitaire = prix.get(fruit, 0)
        sous_total = qte * prix_unitaire
        total += sous_total
        lignes.append({
            "Fruit": f"{EMOJIS.get(fruit, '')} {fruit.capitalize()}",
            "Qté": qte,
            "Prix/unité": f"{prix_unitaire} €",
            "Sous-total": f"{sous_total:.2f} €",
        })

    st.table(lignes)
    st.markdown(f"### Total : **{total:.2f} €**")

    col_vider, _ = st.columns([1, 3])
    with col_vider:
        if st.button("🗑️ Vider le panier"):
            st.session_state.panier = {}
            st.rerun()

    # --- Formulaire de commande ---
    st.divider()
    st.header("📋 Vos informations")

    with st.form("formulaire_commande"):
        Status_RGPD = st.checkbox("J'accepte que mes données soient utilisées pour traiter ma commande (obligatoire)", value=False)
        nom = st.text_input("Nom complet *", placeholder="Ex: Jean Dupont")
        adresse = st.text_input("Adresse de livraison *", placeholder="Ex: 123 Rue des Fruits, 75000 Paris")
        telephone = st.text_input("Téléphone *", placeholder="Ex: +33 07 00 00 00 00")
        note = st.text_area("Note (optionnel)", placeholder="Livraison point relais, allergies particulières...")
        soumettre = st.form_submit_button("✅ Confirmer la commande")

    if soumettre:
        if not nom.strip():
            st.error("Veuillez saisir votre nom.")
        elif not adresse.strip():
            st.error("Veuillez saisir une adresse de livraison.")
        elif not telephone.strip():
            st.error("Veuillez saisir votre numéro de téléphone.")
        else:
            commande = passer_commande(nom.strip(), adresse.strip(), telephone.strip(), dict(st.session_state.panier), prix)
            st.session_state.panier = {}
            st.success(f"Commande **#{commande['id']}** passée avec succès ! Nous vous contacterons au {commande['telephone']} pour confirmer la livraison.")
            st.balloons()
            st.info(f"Total à régler : **{commande['total']:.2f} €**")
            
