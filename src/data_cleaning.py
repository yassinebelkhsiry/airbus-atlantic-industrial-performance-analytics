"""Nettoyage et préparation des données industrielles."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "donnees_production_airbus_atlantic.csv"
PROCESSED_DATA_PATH = ROOT_DIR / "data" / "processed" / "donnees_production_nettoyees.csv"
QUALITY_REPORT_PATH = ROOT_DIR / "data" / "processed" / "rapport_qualite_donnees.csv"


def detecter_anomalies_iqr(df: pd.DataFrame, colonnes: list[str]) -> pd.DataFrame:
    """Ajoute des indicateurs d'anomalies statistiques via la méthode IQR."""
    result = df.copy()
    for colonne in colonnes:
        q1 = result[colonne].quantile(0.25)
        q3 = result[colonne].quantile(0.75)
        iqr = q3 - q1
        borne_basse = q1 - 1.5 * iqr
        borne_haute = q3 + 1.5 * iqr
        result[f"anomalie_stats_{colonne}"] = ~result[colonne].between(borne_basse, borne_haute)
    return result


def nettoyer_donnees(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Nettoie le dataset et retourne aussi un rapport de complétude."""
    rapport_qualite = (
        df.isna()
        .sum()
        .rename("valeurs_manquantes")
        .reset_index()
        .rename(columns={"index": "colonne"})
    )
    rapport_qualite["taux_manquant"] = rapport_qualite["valeurs_manquantes"] / len(df)

    cleaned = df.drop_duplicates(subset=["ordre_fabrication"]).copy()
    cleaned["date_production"] = pd.to_datetime(cleaned["date_production"], errors="coerce")
    cleaned = cleaned.dropna(subset=["date_production", "site", "ligne_production", "type_piece"])

    cleaned["type_anomalie"] = cleaned["type_anomalie"].fillna("Aucune")
    cleaned["gravite_anomalie"] = np.where(cleaned["type_anomalie"] == "Aucune", "Aucune", cleaned["gravite_anomalie"])

    for colonne in ["temps_cycle_min", "temperature_machine", "vibration_machine", "taux_disponibilite_machine"]:
        cleaned[colonne] = cleaned.groupby(["ligne_production", "type_piece"])[colonne].transform(
            lambda serie: serie.fillna(serie.median())
        )

    cleaned["quantite_non_conforme"] = cleaned["quantite_produite"] - cleaned["quantite_conforme"]
    cleaned["taux_conformite"] = cleaned["quantite_conforme"] / cleaned["quantite_produite"]
    cleaned["taux_non_conformite"] = cleaned["quantite_non_conforme"] / cleaned["quantite_produite"]
    cleaned["retard_livraison"] = cleaned["delai_reel_jours"] > cleaned["delai_prevu_jours"]
    cleaned["mois_production"] = cleaned["date_production"].dt.to_period("M").astype(str)
    cleaned["annee_mois"] = cleaned["date_production"].dt.to_period("M").dt.to_timestamp()
    cleaned["productivite_par_heure"] = cleaned["quantite_conforme"] / (cleaned["temps_cycle_min"] / 60)
    cleaned["ecart_delai_jours"] = cleaned["delai_reel_jours"] - cleaned["delai_prevu_jours"]
    cleaned["presence_anomalie"] = cleaned["type_anomalie"] != "Aucune"
    cleaned["anomalie_critique"] = cleaned["gravite_anomalie"] == "Critique"

    cleaned = detecter_anomalies_iqr(
        cleaned,
        ["temps_cycle_min", "cout_non_qualite", "temperature_machine", "vibration_machine"],
    )

    return cleaned, rapport_qualite


def main() -> None:
    df = pd.read_csv(RAW_DATA_PATH, encoding="utf-8")
    cleaned, rapport_qualite = nettoyer_donnees(df)
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_DATA_PATH, index=False, encoding="utf-8")
    rapport_qualite.to_csv(QUALITY_REPORT_PATH, index=False, encoding="utf-8")
    print(f"Données nettoyées : {PROCESSED_DATA_PATH} ({len(cleaned):,} lignes)")
    print(f"Rapport qualité : {QUALITY_REPORT_PATH}")


if __name__ == "__main__":
    main()
