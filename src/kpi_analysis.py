"""Calcul des indicateurs de performance industrielle."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DATA_PATH = ROOT_DIR / "data" / "processed" / "donnees_production_nettoyees.csv"
KPI_GLOBAL_PATH = ROOT_DIR / "data" / "processed" / "kpi_globaux.csv"
KPI_MONTHLY_PATH = ROOT_DIR / "data" / "processed" / "kpi_mensuels.csv"
KPI_LINE_PATH = ROOT_DIR / "data" / "processed" / "kpi_lignes_production.csv"
KPI_ANOMALIES_PATH = ROOT_DIR / "data" / "processed" / "kpi_anomalies.csv"


def calculer_kpi_globaux(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule les KPI principaux suivis par le pilotage opérationnel."""
    total_produit = df["quantite_produite"].sum()
    total_conforme = df["quantite_conforme"].sum()
    total_non_conforme = df["quantite_non_conforme"].sum()

    kpi = {
        "taux_conformite": total_conforme / total_produit,
        "taux_non_conformite": total_non_conforme / total_produit,
        "taux_retard_livraison": df["retard_livraison"].mean(),
        "productivite_moyenne_par_heure": df["productivite_par_heure"].mean(),
        "cout_total_non_qualite": df["cout_non_qualite"].sum(),
        "temps_cycle_moyen_min": df["temps_cycle_min"].mean(),
        "disponibilite_machine_moyenne": df["taux_disponibilite_machine"].mean(),
        "nombre_anomalies": int(df["presence_anomalie"].sum()),
        "anomalies_critiques": int(df["anomalie_critique"].sum()),
        "volume_total_produit": int(total_produit),
    }
    return pd.DataFrame([kpi])


def calculer_kpi_mensuels(df: pd.DataFrame) -> pd.DataFrame:
    """Produit l'évolution mensuelle de la performance."""
    monthly = (
        df.groupby("annee_mois")
        .agg(
            quantite_produite=("quantite_produite", "sum"),
            quantite_conforme=("quantite_conforme", "sum"),
            quantite_non_conforme=("quantite_non_conforme", "sum"),
            taux_retard_livraison=("retard_livraison", "mean"),
            cout_non_qualite=("cout_non_qualite", "sum"),
            temps_cycle_moyen_min=("temps_cycle_min", "mean"),
            disponibilite_machine=("taux_disponibilite_machine", "mean"),
            anomalies_critiques=("anomalie_critique", "sum"),
        )
        .reset_index()
    )
    monthly["taux_conformite"] = monthly["quantite_conforme"] / monthly["quantite_produite"]
    monthly["taux_non_conformite"] = monthly["quantite_non_conforme"] / monthly["quantite_produite"]
    return monthly


def calculer_kpi_lignes(df: pd.DataFrame) -> pd.DataFrame:
    """Synthétise la performance par ligne de production."""
    lines = (
        df.groupby("ligne_production")
        .agg(
            quantite_produite=("quantite_produite", "sum"),
            quantite_conforme=("quantite_conforme", "sum"),
            quantite_non_conforme=("quantite_non_conforme", "sum"),
            taux_retard_livraison=("retard_livraison", "mean"),
            productivite_par_heure=("productivite_par_heure", "mean"),
            cout_non_qualite=("cout_non_qualite", "sum"),
            temps_cycle_moyen_min=("temps_cycle_min", "mean"),
            disponibilite_machine=("taux_disponibilite_machine", "mean"),
            anomalies_critiques=("anomalie_critique", "sum"),
        )
        .reset_index()
    )
    lines["taux_conformite"] = lines["quantite_conforme"] / lines["quantite_produite"]
    lines["taux_non_conformite"] = lines["quantite_non_conforme"] / lines["quantite_produite"]
    return lines.sort_values("cout_non_qualite", ascending=False)


def calculer_kpi_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Compte les anomalies par type et estime leur impact économique."""
    anomalies = df[df["type_anomalie"] != "Aucune"]
    return (
        anomalies.groupby("type_anomalie")
        .agg(
            nombre_anomalies=("type_anomalie", "size"),
            cout_non_qualite=("cout_non_qualite", "sum"),
            temps_cycle_moyen_min=("temps_cycle_min", "mean"),
            anomalies_critiques=("anomalie_critique", "sum"),
        )
        .reset_index()
        .sort_values("nombre_anomalies", ascending=False)
    )


def main() -> None:
    df = pd.read_csv(PROCESSED_DATA_PATH, parse_dates=["date_production", "annee_mois"], encoding="utf-8")
    calculer_kpi_globaux(df).to_csv(KPI_GLOBAL_PATH, index=False, encoding="utf-8")
    calculer_kpi_mensuels(df).to_csv(KPI_MONTHLY_PATH, index=False, encoding="utf-8")
    calculer_kpi_lignes(df).to_csv(KPI_LINE_PATH, index=False, encoding="utf-8")
    calculer_kpi_anomalies(df).to_csv(KPI_ANOMALIES_PATH, index=False, encoding="utf-8")
    print("KPI générés dans data/processed/")


if __name__ == "__main__":
    main()
