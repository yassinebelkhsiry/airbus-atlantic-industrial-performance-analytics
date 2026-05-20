"""Génération d'un dataset industriel synthétique pour l'analyse de performance."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "donnees_production_airbus_atlantic.csv"


def generer_donnees_industrielles(n_lignes: int = 12_000, seed: int = 42) -> pd.DataFrame:
    """Crée un jeu de données réaliste pour le pilotage industriel aéronautique."""
    rng = np.random.default_rng(seed)

    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    sites = ["Casablanca", "Rochefort", "Montoir-de-Bretagne"]
    lignes = ["Ligne A320", "Ligne A330", "Ligne A350", "Ligne Assemblage Cabine", "Ligne Composite"]
    pieces = ["Panneau fuselage", "Cadre structure", "Porte avion", "Plancher cabine", "Sous-ensemble composite"]
    equipes = ["Équipe Alpha", "Équipe Bravo", "Équipe Charlie", "Équipe Delta"]
    shifts = ["Matin", "Après-midi", "Nuit"]
    anomalies = [
        "Aucune",
        "Défaut dimensionnel",
        "Non-conformité matière",
        "Retouche peinture",
        "Écart documentaire",
        "Défaut assemblage",
        "Panne machine",
        "Contrôle qualité bloquant",
    ]
    gravites = ["Aucune", "Mineure", "Majeure", "Critique"]

    site = rng.choice(sites, size=n_lignes, p=[0.58, 0.22, 0.20])
    ligne = rng.choice(lignes, size=n_lignes, p=[0.24, 0.20, 0.22, 0.18, 0.16])
    type_piece = rng.choice(pieces, size=n_lignes, p=[0.24, 0.20, 0.18, 0.18, 0.20])
    date_production = rng.choice(dates, size=n_lignes)

    quantite_produite = rng.poisson(lam=42, size=n_lignes) + rng.integers(8, 35, size=n_lignes)
    complexite = pd.Series(type_piece).map(
        {
            "Panneau fuselage": 1.15,
            "Cadre structure": 1.00,
            "Porte avion": 1.30,
            "Plancher cabine": 0.90,
            "Sous-ensemble composite": 1.25,
        }
    ).to_numpy()
    facteur_ligne = pd.Series(ligne).map(
        {
            "Ligne A320": 0.95,
            "Ligne A330": 1.05,
            "Ligne A350": 1.15,
            "Ligne Assemblage Cabine": 0.90,
            "Ligne Composite": 1.20,
        }
    ).to_numpy()

    taux_defaut = np.clip(rng.normal(0.045 * complexite * facteur_ligne, 0.018, size=n_lignes), 0.002, 0.19)
    quantite_non_conforme = rng.binomial(quantite_produite, taux_defaut)
    quantite_conforme = quantite_produite - quantite_non_conforme

    temps_cycle_min = np.clip(rng.normal(46 * complexite * facteur_ligne, 8.5, size=n_lignes), 18, 110)
    delai_prevu_jours = rng.integers(2, 12, size=n_lignes)
    risque_retard = np.clip(0.18 + taux_defaut * 2.8 + (temps_cycle_min > 65) * 0.12, 0, 0.72)
    retard = rng.binomial(1, risque_retard)
    delai_reel_jours = delai_prevu_jours + retard * rng.integers(1, 7, size=n_lignes) - (1 - retard) * rng.binomial(1, 0.18, size=n_lignes)
    delai_reel_jours = np.maximum(delai_reel_jours, 1)
    statut_livraison = np.where(delai_reel_jours > delai_prevu_jours, "En retard", "À l'heure")

    type_anomalie = []
    gravite_anomalie = []
    for qnc, tcycle, dispo in zip(quantite_non_conforme, temps_cycle_min, rng.normal(0.91, 0.045, n_lignes)):
        if qnc == 0 and rng.random() > 0.08:
            type_anomalie.append("Aucune")
            gravite_anomalie.append("Aucune")
        else:
            choix = rng.choice(anomalies[1:], p=[0.18, 0.13, 0.15, 0.14, 0.18, 0.10, 0.12])
            type_anomalie.append(choix)
            if choix in {"Panne machine", "Contrôle qualité bloquant"} or tcycle > 72 or dispo < 0.84:
                gravite_anomalie.append(rng.choice(["Majeure", "Critique"], p=[0.68, 0.32]))
            else:
                gravite_anomalie.append(rng.choice(gravites[1:], p=[0.58, 0.34, 0.08]))

    gravite_anomalie = np.array(gravite_anomalie)
    type_anomalie = np.array(type_anomalie)
    multiplicateur_gravite = pd.Series(gravite_anomalie).map({"Aucune": 0, "Mineure": 140, "Majeure": 430, "Critique": 950}).to_numpy()
    cout_non_qualite = np.round(quantite_non_conforme * rng.normal(310, 65, n_lignes) + multiplicateur_gravite, 2)
    cout_non_qualite = np.maximum(cout_non_qualite, 0)

    disponibilite = np.clip(
        rng.normal(0.92, 0.045, n_lignes) - (type_anomalie == "Panne machine") * rng.uniform(0.05, 0.15, n_lignes),
        0.62,
        0.995,
    )
    temperature = np.clip(rng.normal(68, 6.5, n_lignes) + (disponibilite < 0.82) * rng.normal(6, 2, n_lignes), 48, 95)
    vibration = np.clip(rng.normal(2.4, 0.55, n_lignes) + (type_anomalie == "Panne machine") * rng.normal(1.1, 0.25, n_lignes), 0.8, 6.2)

    df = pd.DataFrame(
        {
            "date_production": pd.to_datetime(date_production),
            "site": site,
            "ligne_production": ligne,
            "type_piece": type_piece,
            "ordre_fabrication": [f"OF-{2024 + (i % 2)}-{i:06d}" for i in range(1, n_lignes + 1)],
            "quantite_produite": quantite_produite,
            "quantite_conforme": quantite_conforme,
            "quantite_non_conforme": quantite_non_conforme,
            "temps_cycle_min": np.round(temps_cycle_min, 2),
            "delai_prevu_jours": delai_prevu_jours,
            "delai_reel_jours": delai_reel_jours,
            "statut_livraison": statut_livraison,
            "type_anomalie": type_anomalie,
            "gravite_anomalie": gravite_anomalie,
            "cout_non_qualite": cout_non_qualite,
            "operateur_equipe": rng.choice(equipes, size=n_lignes),
            "shift": rng.choice(shifts, size=n_lignes, p=[0.42, 0.38, 0.20]),
            "taux_disponibilite_machine": np.round(disponibilite, 4),
            "temperature_machine": np.round(temperature, 2),
            "vibration_machine": np.round(vibration, 2),
        }
    ).sort_values("date_production")

    # Injection contrôlée de valeurs manquantes pour rendre le nettoyage réaliste.
    for colonne, taux in {"temps_cycle_min": 0.006, "type_anomalie": 0.004, "temperature_machine": 0.005}.items():
        index = rng.choice(df.index, size=int(n_lignes * taux), replace=False)
        df.loc[index, colonne] = np.nan

    return df.reset_index(drop=True)


def main() -> None:
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = generer_donnees_industrielles()
    df.to_csv(RAW_DATA_PATH, index=False, encoding="utf-8")
    print(f"Dataset généré : {RAW_DATA_PATH} ({len(df):,} lignes)")


if __name__ == "__main__":
    main()
