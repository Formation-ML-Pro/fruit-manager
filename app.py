import streamlit as st
from fruit_manager import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


st.set_page_config('Plantation', layout='wide', page_icon="🍇")
st.title("🍇 Dashboard de la Plantation")

inventaire = ouvrir_inventaire()
prix = ouvrir_prix()
tresorerie = ouvrir_tresorerie()
icones = ouvrir_icones()


with st.sidebar:
    st.radio("Devise", options=["$", "€"], key="devise", horizontal=True, label_visibility="hidden")
    st.header("🛒 Vendre des Fruits")
    fruit_vendre = st.selectbox("Choisir un fruit", list(inventaire.keys()))
    quantite_vendre = st.number_input("Quantité a vendre", min_value=1, step=1, max_value=inventaire[fruit_vendre])

    if st.button("Vendre"):
        inventaire, tresorerie, message = vendre(inventaire, fruit_vendre, quantite_vendre, tresorerie, prix)
        st.success(message['text'])

    st.header("🌱 Récolter des Fruits")
    fruit_recolter = st.selectbox("Choisir un fruit à récolter", list(inventaire.keys()), key="recolte_individuelle")
    quantite_recolter = st.number_input("Quantité à récolter", min_value=1, step=1, key="quantite_recolte", max_value=100)

    if st.button("Récolter"):
        inventaire, message = recolter(inventaire, fruit_recolter, quantite_recolter)
        st.success(message['text'])

c1, _, c2 = st.columns([10,1,10])
with c1:

    st.header("💰 Trésorerie",  divider = "grey")
    st.metric(label="Montant disponible", value = f"{tresorerie:.2f} $" if st.session_state.devise == "$" else f"{dollar_to_euro(tresorerie):.2f} €")
    st.markdown("###")

    st.header("📈 Évolution de la trésorerie")
    historique = lire_tresorerie_historique()
    if historique:

        df = pd.DataFrame(historique).tail(20)  # Derniers 20 points
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        if st.session_state.devise == "€":
            df["tresorerie"] = df["tresorerie"] * dollar_to_euro(1)

        fig, ax = plt.subplots()
        ax.plot(df["timestamp"], df["tresorerie"], marker="o")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"Trésorerie ({st.session_state.devise})")
        ax.set_title("Évolution de la trésorerie")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m %H:%M'))
        fig.autofmt_xdate()
        _, mid_col, _ = st.columns([1, 15, 1])
        mid_col.pyplot(fig)
    else:
        st.info("Aucune donnée d'historique de trésorerie pour le moment.")


with c2:

    st.header("📦 Inventaire",  divider = "grey")
    _, sub_c2, _ = st.columns([1, 3, 1])
    # Inventaire sous forme de tableau
    df_inventaire = pd.DataFrame({
        "Fruit": list(inventaire.keys()),
        "": [icones.get(fruit, "") for fruit in inventaire.keys()],  # colonne sans titre avec icônes
        "Quantité": list(inventaire.values())
    }) # DataFrame avec les colonnes spécifique et emoji des fruits
    sub_c2.dataframe(data=df_inventaire, hide_index=True)   # st.dataframe à la place de st.table (plus joli)
    # Inventraire sous forme de graphique
    fig, ax = plt.subplots()
    # Trier l'inventaire par quantité décroissante
    inventaire = dict(sorted(inventaire.items(), key=lambda item: item[1], reverse=True))
    ax.bar(inventaire.keys(), inventaire.values(), color="salmon", edgecolor='k')
    ax.set_xlabel("Fruit")
    ax.tick_params(axis='x', rotation=45)
    ax.set_ylabel("Quantité")
    ax.set_title("Inventaire")
    _, mid_col, _ = st.columns([1, 10, 1])
    mid_col.pyplot(fig)


ecrire_inventaire(inventaire)
ecrire_tresorerie(tresorerie)