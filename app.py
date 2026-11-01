import streamlit as st
import database as db
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

db.creer_tables()
db.importer_json()

def afficher(message):
    if message["status"] == "success":
        st.success(message["text"])
    else:
        st.error(message["text"])

st.title("🍇 Dashboard de la Plantation")
fruits = list(db.lire_prix())

with st.sidebar:
    st.header("🛒 Vendre des Fruits")
    fruit_vendre = st.selectbox("Choisir un fruit", fruits)
    quantite_vendre = st.number_input("Quantité à vendre", min_value=1, step=1)
    client = st.text_input("Client (facultatif)")
    if st.button("Vendre"):
        afficher(db.vendre(fruit_vendre, quantite_vendre, client))

    st.header("🌱 Récolter des Fruits")
    fruit_recolter = st.selectbox("Choisir un fruit à récolter", fruits, key="recolte_individuelle")
    quantite_recolter = st.number_input("Quantité à récolter", min_value=1, step=1, key="quantite_recolte")
    if st.button("Récolter"):
        afficher(db.recolter(fruit_recolter, quantite_recolter))


inventaire = db.lire_inventaire()
tresorerie = db.lire_tresorerie()
historique = db.lire_historique()

st.header("💰 Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie:.2f} $")

st.header("📈 Évolution de la trésorerie")
historique = db.lire_historique()
if historique:

    df = pd.DataFrame(historique).tail(20)  # Derniers 20 points
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601")
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
