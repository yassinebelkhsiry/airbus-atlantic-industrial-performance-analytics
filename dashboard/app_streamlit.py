"""Dashboard Streamlit pour le pilotage de la performance industrielle."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "processed" / "donnees_production_nettoyees.csv"


st.set_page_config(
    page_title="Airbus Atlantic - Performance industrielle",
    page_icon="✈️",
    layout="wide",
)


@st.cache_data
def charger_donnees() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["date_production", "annee_mois"], encoding="utf-8")
    return df


def formatter_pourcentage(valeur: float) -> str:
    return f"{valeur:.1%}"


def afficher_carte_kpi(titre: str, valeur: str, aide: str) -> None:
    st.metric(titre, valeur, help=aide)


df = charger_donnees()

st.title("Pilotage de la performance industrielle")
st.caption("Stage PFE - Data Analyst - Airbus Atlantic, Casablanca")

with st.sidebar:
    st.header("Filtres")
    date_min, date_max = df["date_production"].min().date(), df["date_production"].max().date()
    plage_dates = st.date_input("Période de production", value=(date_min, date_max), min_value=date_min, max_value=date_max)
    sites = st.multiselect("Site", sorted(df["site"].unique()), default=sorted(df["site"].unique()))
    lignes = st.multiselect("Ligne de production", sorted(df["ligne_production"].unique()), default=sorted(df["ligne_production"].unique()))

if len(plage_dates) == 2:
    debut, fin = pd.to_datetime(plage_dates[0]), pd.to_datetime(plage_dates[1])
else:
    debut, fin = df["date_production"].min(), df["date_production"].max()

donnees = df[
    (df["date_production"].between(debut, fin))
    & (df["site"].isin(sites))
    & (df["ligne_production"].isin(lignes))
].copy()

if donnees.empty:
    st.warning("Aucune donnée disponible pour les filtres sélectionnés.")
    st.stop()

total_produit = donnees["quantite_produite"].sum()
taux_conformite = donnees["quantite_conforme"].sum() / total_produit
taux_retard = donnees["retard_livraison"].mean()
cout_non_qualite = donnees["cout_non_qualite"].sum()
disponibilite = donnees["taux_disponibilite_machine"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    afficher_carte_kpi("Taux de conformité", formatter_pourcentage(taux_conformite), "Pièces conformes / pièces produites")
with col2:
    afficher_carte_kpi("Taux de retard", formatter_pourcentage(taux_retard), "Ordres livrés au-delà du délai prévu")
with col3:
    afficher_carte_kpi("Volume produit", f"{total_produit:,.0f}".replace(",", " "), "Quantité totale produite")
with col4:
    afficher_carte_kpi("Coût non-qualité", f"{cout_non_qualite:,.0f} €".replace(",", " "), "Coûts liés aux non-conformités")
with col5:
    afficher_carte_kpi("Disponibilité machine", formatter_pourcentage(disponibilite), "Moyenne des taux de disponibilité")

mensuel = (
    donnees.groupby("annee_mois")
    .agg(
        quantite_produite=("quantite_produite", "sum"),
        quantite_conforme=("quantite_conforme", "sum"),
        cout_non_qualite=("cout_non_qualite", "sum"),
        taux_retard=("retard_livraison", "mean"),
    )
    .reset_index()
)
mensuel["taux_conformite"] = mensuel["quantite_conforme"] / mensuel["quantite_produite"]

ligne = (
    donnees.groupby("ligne_production")
    .agg(
        quantite_produite=("quantite_produite", "sum"),
        taux_retard=("retard_livraison", "mean"),
        cout_non_qualite=("cout_non_qualite", "sum"),
        productivite=("productivite_par_heure", "mean"),
    )
    .reset_index()
)

tab_perf, tab_anomalies, tab_recommandations = st.tabs(["Performance", "Anomalies critiques", "Recommandations"])

with tab_perf:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(
            mensuel,
            x="annee_mois",
            y="taux_conformite",
            markers=True,
            title="Évolution mensuelle du taux de conformité",
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(
            ligne.sort_values("quantite_produite", ascending=False),
            x="quantite_produite",
            y="ligne_production",
            orientation="h",
            title="Volume produit par ligne",
        )
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = px.bar(
            ligne.sort_values("taux_retard", ascending=False),
            x="taux_retard",
            y="ligne_production",
            orientation="h",
            title="Retards par ligne de production",
        )
        fig.update_xaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = px.line(
            mensuel,
            x="annee_mois",
            y="cout_non_qualite",
            markers=True,
            title="Coût de non-qualité par mois",
        )
        st.plotly_chart(fig, use_container_width=True)

with tab_anomalies:
    anomalies = donnees[donnees["type_anomalie"] != "Aucune"]
    top_anomalies = anomalies["type_anomalie"].value_counts().reset_index()
    top_anomalies.columns = ["type_anomalie", "nombre"]
    fig = px.bar(top_anomalies, x="nombre", y="type_anomalie", orientation="h", title="Top anomalies")
    st.plotly_chart(fig, use_container_width=True)

    critiques = donnees[donnees["anomalie_critique"]].sort_values("cout_non_qualite", ascending=False)
    st.subheader("Tableau des anomalies critiques")
    st.dataframe(
        critiques[
            [
                "date_production",
                "site",
                "ligne_production",
                "type_piece",
                "ordre_fabrication",
                "type_anomalie",
                "cout_non_qualite",
                "temps_cycle_min",
                "ecart_delai_jours",
            ]
        ].head(100),
        use_container_width=True,
        hide_index=True,
    )

with tab_recommandations:
    ligne_retard = ligne.sort_values("taux_retard", ascending=False).iloc[0]
    ligne_cout = ligne.sort_values("cout_non_qualite", ascending=False).iloc[0]
    st.markdown(
        f"""
        ### Recommandations métier

        - Prioriser un plan d'action court terme sur **{ligne_retard['ligne_production']}**, ligne présentant le taux de retard le plus élevé sur le périmètre filtré.
        - Renforcer le contrôle amont sur **{ligne_cout['ligne_production']}**, principal contributeur au coût de non-qualité.
        - Suivre quotidiennement les anomalies critiques avec un rituel qualité-production pour accélérer les décisions de blocage, retouche ou libération.
        - Croiser les signaux machine, notamment température et vibration, avec les défauts d'assemblage et les pannes machine pour anticiper les dérives.
        - Mettre en place un seuil d'alerte automatique lorsque le taux de conformité passe sous 95 % ou lorsque le retard dépasse 30 %.
        """
    )
