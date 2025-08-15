# pages/01_Plantations.py
import os, json
import pandas as pd
import streamlit as st
import plotly.express as px
from fruit import creer_fruits, lire_fruits 
from plantation import creer_plantation
from datetime import datetime
from zoneinfo import ZoneInfo



PLANTATIONS_PATH = "data/plantations.json"
FRUIT_ICONS = {f["nom"]: f.get("icone", "❓") for f in lire_fruits()}
JOURS_FR = ["Lun","Mar","Mer","Jeu","Ven","Sam","Dim"]
MOIS_FR  = ["Jan","Fév","Mars","Avril","Mai","Juin","Juil","Août","Sep","Oct","Nov","Déc"]
CLIMAT_COLORS = {
    "tropical":      "#D81B60",  # rose vif
    "subtropical":   "#8E24AA",  # violet
    "méditerranéen": "#F4511E",  # orange soutenu
    "tempéré":       "#FFB300",  # jaune orangé
    "froid":         "#5D4037",  # brun foncé
}



def format_date_fr(iso_str: str) -> str:
    if not iso_str:
        return ""
    try:
        s = iso_str.replace("Z", "+00:00")  # support éventuel des dates ISO en Z
        dt = datetime.fromisoformat(s)
        tz = ZoneInfo("Europe/Brussels")
        dt = dt.astimezone(tz) if dt.tzinfo else dt.replace(tzinfo=tz)
        return f"{dt.hour:02d}h{dt.minute:02d}, {JOURS_FR[dt.weekday()]} {dt.day:02d} {MOIS_FR[dt.month-1]} {dt.year}"
    except Exception:
        return iso_str
    
    

st.set_page_config(page_title="Plantations", page_icon="🌍", layout="wide")
st.title("🌍 Carte & liste des plantations")

@st.cache_data(show_spinner=False)
def charger_plantations(path: str) -> pd.DataFrame:
    """
    Lit le JSON des plantations et retourne un DataFrame aplati :
    colonnes: lat, lon, climat, superficie_m2, date_creation, fruits_count, fruits_list
    """
    if not os.path.exists(path):
        return pd.DataFrame(columns=[
            "lat","lon","climat","superficie_m2","date_creation","fruits_count","fruits_list"
        ])
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return pd.DataFrame(columns=[
            "lat","lon","climat","superficie_m2","date_creation","fruits_count","fruits_list"
        ])

    rows = []
    for p in data:
        geoloc = p.get("geoloc", {})
        lat = geoloc.get("lat")
        lon = geoloc.get("lon")
        climat = p.get("climat")
        superficie = (
            p.get("superficie_totale [m\u00B2]")
            or p.get("superficie_totale")
            or 0
        )
        date_creation = p.get("date_creation")
        fruits = p.get("fruits_plantés", {}) or {}

        fruits_noms = list(fruits.keys())
        fruits_count = len(fruits_noms)
        fruits_list = ", ".join(fruits_noms)

        rows.append({
            "lat": lat,
            "lon": lon,
            "climat": climat,
            "superficie_m2": float(superficie) if superficie is not None else 0.0,
            "date_creation": date_creation,
            "fruits_count": fruits_count,
            "fruits_list": " ".join(FRUIT_ICONS.get(n, "❓") for n in fruits_noms),

        })
    df = pd.DataFrame(rows)
    # Nettoyage minimal
    df = df.dropna(subset=["lat","lon"]).reset_index(drop=True)
    return df

df = charger_plantations(PLANTATIONS_PATH)

# Bandeau d'infos
col1, col2, col3 = st.columns(3)
col1.metric("Plantations", f"{len(df):,}".replace(",", " "))
col2.metric("Superficie totale (m²)", f"{int(df['superficie_m2'].sum()):,}".replace(",", " "))
col3.metric("Climats", f"{df['climat'].nunique() if not df.empty else 0}")

st.divider()

# Filtres
with st.expander("🔎 Filtres", expanded=True):
    c1, c2, c3 = st.columns([1,1,2])
    climats = sorted([c for c in df["climat"].dropna().unique()]) if not df.empty else []
    filtre_climat = c1.multiselect("Climat", options=climats, default=climats)

    min_sup, max_sup = (0, 0)
    if not df.empty:
        min_sup, max_sup = int(df["superficie_m2"].min()), int(df["superficie_m2"].max())
    filtre_sup = c2.slider("Superficie (m²)", min_value=min_sup, max_value=max_sup if max_sup>0 else 0,
                           value=(min_sup, max_sup if max_sup>0 else 0), step=1)

    filtre_texte = c3.text_input("Rechercher (fruits, climat…)", value="")

# Application des filtres
df_f = df.copy()
if df_f.empty:
    st.info("Aucune plantation trouvée. Crée une plantation pour voir la carte et la liste.")
else:
    if filtre_climat:
        df_f = df_f[df_f["climat"].isin(filtre_climat)]
    if filtre_sup[1] > 0:
        df_f = df_f[(df_f["superficie_m2"] >= filtre_sup[0]) & (df_f["superficie_m2"] <= filtre_sup[1])]
    if filtre_texte.strip():
        q = filtre_texte.strip().lower()
        df_f = df_f[df_f.apply(lambda r: q in str(r["fruits_list"]).lower()
                                          or q in str(r["climat"]).lower()
                                          or q in str(r["date_creation"]).lower(), axis=1)]

    # Carte Plotly
    st.subheader("🗺️ Localisation des plantations")
    if df_f.empty:
        st.warning("Aucun résultat avec ces filtres.")
    else:
       # Hover riche (inchangé)
        df_f = df_f.assign(
            hover=df_f.apply(lambda r: f"Climat: {r['climat']}<br>"
                                    f"Superficie: {int(r['superficie_m2'])} m²<br>"
                                    f"Fruits: {r['fruits_list']}<br>"
                                    f"Créée: {r['date_creation']}", axis=1)
        )

        # Figure + palette + libellés
        fig = px.scatter_geo(
            df_f,
            lat="lat",
            lon="lon",
            color="climat",
            size="superficie_m2",
            hover_name="fruits_list",
            hover_data={"lat": True, "lon": True, "superficie_m2": True, "climat": True, "hover": False},
            custom_data=["hover"],                       # ← nécessaire pour hovertemplate
            projection="natural earth",
            color_discrete_map=CLIMAT_COLORS,
            category_orders={"climat": list(CLIMAT_COLORS.keys())},  # ordre stable
            labels={"climat": "Climat"},                # titre de légende propre
        )

        # Assure le texte dans la légende (si name est vide, on reprend le legendgroup = valeur de climat)
        fig.update_layout(showlegend=True, legend_title_text="Climat")
        fig.for_each_trace(lambda t: t.update(name=str(t.name or t.legendgroup)))

        # Couleurs du globe
        fig.update_geos(
            showland=True,  landcolor="#EDE8D5",
            showocean=True, oceancolor="#D7ECFF",
            showlakes=True, lakecolor="#D7ECFF",
            showcountries=True, countrycolor="rgba(50,50,50,0.25)", countrywidth=0.6,
            showcoastlines=True, coastlinecolor="rgba(50,50,50,0.35)", coastlinewidth=0.8,
        )

        # Contraste des marqueurs + fond
        fig.update_traces(marker=dict(line=dict(width=0.8, color="white"), opacity=0.95))
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
        fig.update_layout(legend_font_color="black")
        
        # Occupe tout l'espace dispo + pas de marges superflues
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=560,
            geo=dict(domain=dict(x=[0, 1], y=[0, 1]))  # pleine hauteur/largeur
        )

        # Grossit légèrement le globe pour réduire l'espace perdu (ajuste si besoin 1.05–1.25)
        fig.update_geos(
            projection_scale=1.18,           # ↑ augmente jusqu’à frôler les bords
            center=dict(lat=15, lon=0),      # centre “neutre” monde
        )


        st.plotly_chart(fig, use_container_width=True)
        

    st.subheader("📋 Liste des plantations")
    # Colonnes utiles
    df_view = df_f.copy().rename(columns={
        "lat": "Latitude",
        "lon": "Longitude",
        "climat": "Climat",
        "superficie_m2": "Superficie [m²]",
        "fruits_count": "Variétés",
        "fruits_list": "Liste des fruits",
    })
    colonnes = ["Latitude","Longitude","Climat","Superficie [m²]","Variétés","Liste des fruits","Date de création"]
    # Colonne de date formatée pour l'affichage
    df_view = df_view.assign(**{"Date de création": df_f["date_creation"].apply(format_date_fr)})
    st.dataframe(
        df_view[colonnes] if not df_view.empty else df_view,
        use_container_width=True,
        height=400
    )

    # Export rapide
    cdl1, cdl2 = st.columns(2)
    cdl1.download_button(
        "Télécharger CSV",
        df_view[colonnes].to_csv(index=False).encode("utf-8"),
        file_name="plantations.csv",
        mime="text/csv",
    )
    cdl2.download_button(
        "Télécharger JSON",
        df_view[colonnes].to_json(orient="records", force_ascii=False).encode("utf-8"),
        file_name="plantations.json",
        mime="application/json",
    )



#--------------------------------------------------------------------------#
#     Plantation de tests. Peuvent être ajouté et supprimée par après!     #
#--------------------------------------------------------------------------#

with st.expander("🧪 Création, suppression d'un ensemble de plantations test", expanded=False):
    c1, c2 = st.columns(2)

    if c1.button("➕ Ajouter plantations de test"):
        import time, random

        # S'assure que le catalogue de fruits existe (le print dans le terminal vient d’ici)
        try:
            creer_fruits()
        except Exception:
            pass

        seeds = [
            (50.5667,   4.1667),   # Ecaussinnes (BE)
            (50.8503,   4.3517),   # Bruxelles (BE)
            (40.8350,  14.5000),   # Près du Vésuve (IT)
            (48.8566,   2.3522),   # Paris (EU)
            (40.7128, -74.0060),   # New York (NA)
            (-23.5505, -46.6333),  # São Paulo (SA)
            (30.0444,  31.2357),   # Le Caire (AF)
            (-33.8688, 151.2093),  # Sydney (OC)
            (35.6895, 139.6917),   # Tokyo (AS)
            (19.4326, -99.1332),   # Mexico (NA)
            (-1.286389, 36.817223),# Nairobi (AF)
            (1.3521,  103.8198),   # Singapour (AS)
            (25.2048,  55.2708),   # Dubaï (AS)
            (19.0760,  72.8777),   # Mumbai (AS)
            (-12.0464, -77.0428),  # Lima (SA)
            (-34.6037, -58.3816),  # Buenos Aires (SA)
            (-33.9249,  18.4241),  # Le Cap (AF)
            (6.5244,     3.3792),  # Lagos (AF)
            (40.4168,   -3.7038),  # Madrid (EU)
            (41.0082,   28.9784),  # Istanbul (EU/AS)
            (55.7558,   37.6173),  # Moscou (EU/AS)
            (51.5074,   -0.1278),  # Londres (EU)
            (37.5665,  126.9780),  # Séoul (AS)
        ]

        logs = []
        for (lat0, lon0) in seeds:
            lat, lon = lat0, lon0
            created = False
            last_msg = ""
            # On tente jusqu'à 3 fois en cas d'échec terre_ferme / rate-limit
            for _ in range(3):
                plantation, msg = creer_plantation(lat, lon)
                last_msg = msg
                if plantation:
                    # Marque is_test=True pour pouvoir nettoyer ensuite
                    try:
                        with open(PLANTATIONS_PATH, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        # Cherche l'entrée correspondante (coords proches + même date_creation)
                        for p in reversed(data):
                            g = p.get("geoloc", {})
                            if (
                                abs(g.get("lat", 9999) - plantation["geoloc"]["lat"]) < 1e-4
                                and abs(g.get("lon", 9999) - plantation["geoloc"]["lon"]) < 1e-4
                                and p.get("date_creation") == plantation["date_creation"]
                            ):
                                p["is_test"] = True
                                break
                        with open(PLANTATIONS_PATH, "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        logs.append(f"OK: {msg}")
                    except Exception as e:
                        logs.append(f"OK (non marqué test): {msg} — {e}")
                    created = True
                    break
                # petit jitter + pause (politesse Nominatim)
                lat = lat0 + random.uniform(-0.2, 0.2)
                lon = lon0 + random.uniform(-0.2, 0.2)
                time.sleep(1.0)
            if not created:
                logs.append(f"ÉCHEC: {last_msg}")

        # Rafraîchit le cache puis rerun, tout en gardant un message persistant
        try:
            charger_plantations.clear()
        except Exception:
            pass
        st.session_state.flash_logs = logs
        st.session_state.flash_kind = "success"
        st.rerun()

    if c2.button("♻️ Réinitialiser (supprimer plantations de test)"):
        if os.path.exists(PLANTATIONS_PATH):
            try:
                with open(PLANTATIONS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = []
            data = [p for p in data if not p.get("is_test", False)]
            with open(PLANTATIONS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            msg = "Plantations de test supprimées."
        else:
            msg = "Aucun fichier de plantations à nettoyer."

        try:
            charger_plantations.clear()
        except Exception:
            pass
        st.session_state.flash_logs = [msg]
        st.session_state.flash_kind = "warning"
        st.rerun()
