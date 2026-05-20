"""Création des visualisations de reporting industriel."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DATA_PATH = ROOT_DIR / "data" / "processed" / "donnees_production_nettoyees.csv"
FIGURES_DIR = ROOT_DIR / "reports" / "figures"


plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("Set2")


def _sauvegarder(nom_fichier: str) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / nom_fichier, dpi=180, bbox_inches="tight")
    plt.close()


def creer_visualisations(df: pd.DataFrame) -> None:
    """Génère les graphiques clés du projet."""
    monthly = (
        df.groupby("annee_mois")
        .agg(
            quantite_produite=("quantite_produite", "sum"),
            quantite_conforme=("quantite_conforme", "sum"),
            cout_non_qualite=("cout_non_qualite", "sum"),
        )
        .reset_index()
    )
    monthly["taux_conformite"] = monthly["quantite_conforme"] / monthly["quantite_produite"]

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=monthly, x="annee_mois", y="taux_conformite", marker="o", linewidth=2.5)
    plt.title("Évolution mensuelle du taux de conformité")
    plt.xlabel("Mois")
    plt.ylabel("Taux de conformité")
    plt.gca().yaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    _sauvegarder("evolution_mensuelle_taux_conformite.png")

    plt.figure(figsize=(11, 5))
    volumes = df.groupby("ligne_production")["quantite_produite"].sum().sort_values(ascending=False)
    sns.barplot(x=volumes.values, y=volumes.index)
    plt.title("Volume produit par ligne de production")
    plt.xlabel("Quantité produite")
    plt.ylabel("Ligne de production")
    _sauvegarder("volume_produit_par_ligne.png")

    plt.figure(figsize=(11, 5))
    anomalies = df[df["type_anomalie"] != "Aucune"]["type_anomalie"].value_counts().head(8)
    sns.barplot(x=anomalies.values, y=anomalies.index)
    plt.title("Top anomalies de production")
    plt.xlabel("Nombre d'occurrences")
    plt.ylabel("Type d'anomalie")
    _sauvegarder("top_anomalies.png")

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=monthly, x="annee_mois", y="cout_non_qualite", marker="o", color="#C44E52", linewidth=2.5)
    plt.title("Coût de non-qualité par mois")
    plt.xlabel("Mois")
    plt.ylabel("Coût de non-qualité")
    _sauvegarder("cout_non_qualite_par_mois.png")

    plt.figure(figsize=(11, 5))
    retards = df.groupby("ligne_production")["retard_livraison"].mean().sort_values(ascending=False)
    sns.barplot(x=retards.values, y=retards.index, color="#DD8452")
    plt.title("Taux de retard par ligne de production")
    plt.xlabel("Taux de retard")
    plt.ylabel("Ligne de production")
    plt.gca().xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
    _sauvegarder("retards_par_ligne_production.png")

    colonnes_corr = [
        "quantite_produite",
        "quantite_non_conforme",
        "temps_cycle_min",
        "delai_reel_jours",
        "cout_non_qualite",
        "taux_disponibilite_machine",
        "temperature_machine",
        "vibration_machine",
    ]
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[colonnes_corr].corr(), annot=True, fmt=".2f", cmap="RdYlGn_r", center=0, square=True)
    plt.title("Heatmap de corrélation des variables industrielles")
    _sauvegarder("heatmap_correlation.png")

    plt.figure(figsize=(11, 5))
    sns.histplot(df["temps_cycle_min"], bins=45, kde=True, color="#4C72B0")
    plt.title("Distribution des temps de cycle")
    plt.xlabel("Temps de cycle (minutes)")
    plt.ylabel("Nombre d'ordres de fabrication")
    _sauvegarder("distribution_temps_cycle.png")


def main() -> None:
    df = pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["date_production", "annee_mois"], encoding="utf-8")
    creer_visualisations(df)
    print(f"Visualisations générées : {FIGURES_DIR}")


if __name__ == "__main__":
    main()
