import streamlit as st
from fruit_manager import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


st.title("🍇 Dashboard de la Plantation")

inventaire = ouvrir_inventaire()
prix = ouvrir_prix()
tresorerie = ouvrir_tresorerie()

with st.sidebar:
    st.header("🛒 Vendre des Fruits")
    fruit_vendre = st.selectbox("Choisir un fruit", list(inventaire.keys()))
    quantite_vendre = st.number_input("Quantité a vendre", min_value=1, step=1)

    if st.button("Vendre"):
        inventaire, tresorerie, message = vendre(inventaire, fruit_vendre, quantite_vendre, tresorerie, prix)
        st.success(message['text'])

    st.header("🌱 Récolter des Fruits")
    fruit_recolter = st.selectbox("Choisir un fruit à récolter", list(inventaire.keys()), key="recolte_individuelle")
    quantite_recolter = st.number_input("Quantité à récolter", min_value=1, step=1, key="quantite_recolte")

    if st.button("Récolter"):
        inventaire, message = recolter(inventaire, fruit_recolter, quantite_recolter)
        st.success(message['text'])


st.header("💰 Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie:.2f} $")

st.header("📈 Évolution de la trésorerie")
historique = lire_tresorerie_historique()
if historique:

    df = pd.DataFrame(historique).tail(20)  # Derniers 20 points
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["tresorerie"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Trésorerie ($)")
    ax.set_title("Évolution de la trésorerie")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
    fig.autofmt_xdate()
    _, mid_col, _ = st.columns([1, 2, 1])
    mid_col.pyplot(fig)
else:
    st.info("Aucune donnée d'historique de trésorerie pour le moment.")


st.header("📦 Inventaire")
# Inventaire sous forme de tableau
st.table(inventaire)
# Inventraire sous forme de graphique
fig, ax = plt.subplots()
# Trier l'inventaire par quantité décroissante
inventaire = dict(sorted(inventaire.items(), key=lambda item: item[1], reverse=True))
ax.bar(inventaire.keys(), inventaire.values(), color="salmon", edgecolor='k')
ax.set_xlabel("Fruit")
ax.set_ylabel("Quantité")
ax.set_title("Inventaire")
st.pyplot(fig)


ecrire_inventaire(inventaire)
ecrire_tresorerie(tresorerie)

# Gestion des commandes  
st.divider()
st.header("📋 Gestion des commandes clients")

commandes = lire_commandes()
en_attente = [c for c in commandes if c["statut"] == "en_attente"]
validees = [c for c in commandes if c["statut"] == "validée"]
annulees = [c for c in commandes if c["statut"] == "annulée"]
ca_commandes = sum(c["total"] for c in validees)

# Métriques rapides
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("⏳ En attente", len(en_attente))
col_m2.metric("✅ Validées", len(validees))
col_m3.metric("❌ Annulées", len(annulees))
col_m4.metric("💵 CA commandes", f"{ca_commandes:.2f} $")

tab_attente, tab_historique, tab_nouvelle, tab_stats = st.tabs(
    ["⏳ En attente", "📂 Historique", "➕ Nouvelle commande", "📊 Statistiques"]
)


# Onglet : Commandes en attente
with tab_attente:
    if not en_attente:
        st.info("Aucune commande en attente.")
    else:
        st.markdown(f"**{len(en_attente)} commande(s) à traiter**")
        for commande in en_attente:
            with st.expander(
                f"📦 #{commande['id']} — {commande['client']} — {commande['total']:.2f} $  |  {commande['timestamp'][:10]}"
            ):
                col_info, col_panier = st.columns([1, 1])
                with col_info:
                    st.markdown("**Informations client**")
                    st.markdown(f"- Nom : {commande['client']}")
                    st.markdown(f"- Téléphone : {commande['telephone']}")
                    st.markdown(f"- Adresse : {commande.get('adresse', '—')}")
                    st.markdown(f"- Date : {commande['timestamp'][:16].replace('T', ' à ')}")
                with col_panier:
                    st.markdown("**Détail du panier**")
                    for fruit, qte in commande["panier"].items():
                        prix_fruit = prix.get(fruit, 0)
                        st.markdown(f"- {fruit.capitalize()} × {qte}  ({prix_fruit * qte:.2f} $)")
                    st.markdown(f"**Total : {commande['total']:.2f} $**")

                col_valider, col_annuler = st.columns(2)
                with col_valider:
                    if st.button("✅ Valider la commande", key=f"valider_{commande['id']}"):
                        inv = ouvrir_inventaire()
                        tres = ouvrir_tresorerie()
                        inv, tres, msg = valider_commande(commande["id"], inv, tres, prix)
                        if msg["status"] == "success":
                            ecrire_inventaire(inv)
                            ecrire_tresorerie(tres)
                            st.success(msg["text"])
                            st.rerun()
                        else:
                            st.error(msg["text"])
                with col_annuler:
                    if st.button("❌ Annuler la commande", key=f"annuler_{commande['id']}"):
                        msg = annuler_commande(commande["id"])
                        if msg["status"] == "success":
                            st.warning(msg["text"])
                            st.rerun()
                        else:
                            st.error(msg["text"])

# Onglet : Historique complet 
with tab_historique:
    if not commandes:
        st.info("Aucune commande enregistrée.")
    else:
        filtre_statut = st.selectbox(
            "Filtrer par statut",
            ["Toutes", "en_attente", "validée", "annulée"],
            key="filtre_historique"
        )
        commandes_filtrees = commandes if filtre_statut == "Toutes" else [
            c for c in commandes if c["statut"] == filtre_statut
        ]

        filtre_client = st.text_input("Rechercher par nom client", key="filtre_client").strip().lower()
        if filtre_client:
            commandes_filtrees = [c for c in commandes_filtrees if filtre_client in c["client"].lower()]

        st.markdown(f"**{len(commandes_filtrees)} commande(s) affichée(s)**")

        for commande in sorted(commandes_filtrees, key=lambda c: c["timestamp"], reverse=True):
            statut_icon = {"en_attente": "⏳", "validée": "✅", "annulée": "❌"}.get(commande["statut"], "•")
            with st.expander(
                f"{statut_icon} #{commande['id']} — {commande['client']} — {commande['total']:.2f} $  |  {commande['timestamp'][:10]}"
            ):
                col_i, col_p = st.columns([1, 1])
                with col_i:
                    st.markdown(f"- **Client :** {commande['client']}")
                    st.markdown(f"- **Téléphone :** {commande['telephone']}")
                    st.markdown(f"- **Adresse :** {commande.get('adresse', '—')}")
                    st.markdown(f"- **Date :** {commande['timestamp'][:16].replace('T', ' à ')}")
                    st.markdown(f"- **Statut :** `{commande['statut']}`")
                with col_p:
                    st.markdown("**Panier :**")
                    for fruit, qte in commande["panier"].items():
                        st.markdown(f"- {fruit.capitalize()} × {qte}")
                    st.markdown(f"**Total : {commande['total']:.2f} $**")

# Onglet : Saisir une nouvelle commande
with tab_nouvelle:
    st.markdown("Enregistrez ici une commande passée par un client (téléphone, sur place, etc.)")
    with st.form("form_nouvelle_commande"):
        st.subheader("Informations client")
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            nom_client = st.text_input("Nom du client")
            telephone = st.text_input("Téléphone")
        with col_n2:
            adresse = st.text_input("Adresse / Localité")

        st.subheader("Panier")
        panier = {}
        cols_fruits = st.columns(len(inventaire))
        for i, (fruit, stock) in enumerate(inventaire.items()):
            with cols_fruits[i]:
                qte = st.number_input(
                    f"{fruit.capitalize()}\n(stock: {stock})",
                    min_value=0,
                    max_value=stock,
                    step=1,
                    key=f"panier_{fruit}"
                )
                if qte > 0:
                    panier[fruit] = qte

        total_preview = sum(panier.get(f, 0) * prix.get(f, 0) for f in panier)
        st.markdown(f"**Total estimé : {total_preview:.2f} $**")

        submitted = st.form_submit_button("📝 Enregistrer la commande")
        if submitted:
            if not nom_client.strip():
                st.error("Le nom du client est obligatoire.")
            elif not panier:
                st.error("Le panier est vide. Sélectionnez au moins un fruit.")
            else:
                commande = passer_commande(nom_client.strip(), adresse.strip(), telephone.strip(), panier, prix)
                st.success(f"Commande #{commande['id']} enregistrée pour {nom_client} — Total : {commande['total']:.2f} $")
                st.rerun()

# Onglet : Statistiques commandes
with tab_stats:
    if not commandes:
        st.info("Pas encore de données de commandes.")
    else:
        st.subheader("Résumé des commandes")
        col_s1, col_s2 = st.columns(2)

        with col_s1:
            # Répartition par statut
            labels = ["En attente", "Validées", "Annulées"]
            sizes = [len(en_attente), len(validees), len(annulees)]
            if any(s > 0 for s in sizes):
                fig_pie, ax_pie = plt.subplots()
                ax_pie.pie(
                    [s for s in sizes if s > 0],
                    labels=[l for l, s in zip(labels, sizes) if s > 0],
                    autopct="%1.0f%%",
                    colors=["#f0a500", "#4caf50", "#f44336"]
                )
                ax_pie.set_title("Répartition par statut")
                st.pyplot(fig_pie)

        with col_s2:
            # Fruits les plus commandés (commandes validées)
            compteur_fruits = {}
            for c in validees:
                for fruit, qte in c["panier"].items():
                    compteur_fruits[fruit] = compteur_fruits.get(fruit, 0) + qte
            if compteur_fruits:
                compteur_fruits = dict(sorted(compteur_fruits.items(), key=lambda x: x[1], reverse=True))
                fig_bar, ax_bar = plt.subplots()
                ax_bar.bar(compteur_fruits.keys(), compteur_fruits.values(), color="steelblue", edgecolor="k")
                ax_bar.set_xlabel("Fruit")
                ax_bar.set_ylabel("Quantité vendue")
                ax_bar.set_title("Fruits les plus commandés (validés)")
                st.pyplot(fig_bar)

        # Top clients
        if validees:
            st.subheader("Top clients (CA validé)")
            ca_clients = {}
            for c in validees:
                ca_clients[c["client"]] = ca_clients.get(c["client"], 0) + c["total"]
            ca_clients = dict(sorted(ca_clients.items(), key=lambda x: x[1], reverse=True))
            df_clients = pd.DataFrame(
                {"Client": list(ca_clients.keys()), "CA (validé) $": [round(v, 2) for v in ca_clients.values()]}
            )
            st.dataframe(df_clients, use_container_width=True, hide_index=True)
