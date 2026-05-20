"""Génération du rapport PFE Markdown et PDF avec visuels premium."""

from __future__ import annotations

from pathlib import Path
from shutil import copyfile
from textwrap import dedent

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.platypus.tableofcontents import TableOfContents


ROOT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
ASSETS_DIR = REPORTS_DIR / "assets"
PDF_PATH = REPORTS_DIR / "rapport_stage_airbus_atlantic.pdf"
MD_PATH = REPORTS_DIR / "rapport_stage_airbus_atlantic.md"
ROOT_PDF_PATH = ROOT_DIR / "rapport_stage_airbus_atlantic.pdf"
ROOT_MD_PATH = ROOT_DIR / "rapport_stage_airbus_atlantic.md"

TITLE = "Développement d'une solution de pilotage et d'analyse de performance industrielle basée sur la Data Analytics chez Airbus Atlantic Casablanca"
AUTHOR = "Yassine BEL-KHSIRY"
SCHOOL = "FST Mohammedia - Faculté des Sciences et Techniques Mohammedia"
SUPERVISOR = "Monsieur Abdelhak Fahsi"
COMPANY = "Airbus Atlantic - Casablanca"
YEAR = "Année universitaire 2025-2026"

BLUE = "#173B6D"
BLUE2 = "#2F80ED"
GREY = "#5F6B7A"
METAL = "#D7DEE8"
BG = "#F5F8FC"
DARK = "#17202A"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(ROOT_DIR / "data" / "processed" / "donnees_production_nettoyees.csv", parse_dates=["date_production", "annee_mois"])
    kpi = pd.read_csv(ROOT_DIR / "data" / "processed" / "kpi_globaux.csv")
    lines = pd.read_csv(ROOT_DIR / "data" / "processed" / "kpi_lignes_production.csv")
    anomalies = pd.read_csv(ROOT_DIR / "data" / "processed" / "kpi_anomalies.csv")
    return df, kpi, lines, anomalies


def fmt_pct(value: float) -> str:
    return f"{value:.1%}".replace(".", ",")


def fmt_num(value: float) -> str:
    return f"{value:,.0f}".replace(",", " ")


def canvas_base(path: Path, title: str, subtitle: str | None = None) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(14, 8), dpi=180)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 14, 8, color=BG))
    ax.add_patch(Rectangle((0, 7.25), 14, 0.75, color=BLUE))
    ax.text(0.55, 7.62, title, color="white", fontsize=17, weight="bold", va="center")
    if subtitle:
        ax.text(0.55, 7.18, subtitle, color=GREY, fontsize=10, va="top")
    return fig, ax


def save(fig: plt.Figure, path: Path) -> Path:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return path


def draw_plane(ax, x=7.0, y=4.4, scale=1.0, color=BLUE):
    ax.add_patch(FancyBboxPatch((x - 2.2 * scale, y - 0.18 * scale), 4.4 * scale, 0.36 * scale, boxstyle="round,pad=0.02,rounding_size=0.18", facecolor=color, edgecolor="none"))
    ax.add_patch(Polygon([[x - 0.2 * scale, y], [x + 1.25 * scale, y + 1.05 * scale], [x + 0.65 * scale, y + 0.08 * scale]], color=BLUE2))
    ax.add_patch(Polygon([[x - 0.45 * scale, y - 0.04 * scale], [x - 1.65 * scale, y - 0.95 * scale], [x - 0.9 * scale, y - 0.10 * scale]], color=BLUE2))
    ax.add_patch(Polygon([[x + 2.15 * scale, y], [x + 2.95 * scale, y + 0.58 * scale], [x + 2.05 * scale, y + 0.18 * scale]], color=color))
    for wx in [-1.3, -0.8, -0.3, 0.2, 0.7, 1.2]:
        ax.add_patch(Circle((x + wx * scale, y), 0.035 * scale, color="white"))


def create_cover() -> Path:
    path = ASSETS_DIR / "couverture_premium_airbus_atlantic.png"
    fig, ax = plt.subplots(figsize=(14, 8), dpi=180)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 14, 8, color="#F8FBFF"))
    ax.add_patch(Polygon([[0, 0], [14, 0], [14, 8], [9.2, 8]], color="#E4ECF6"))
    ax.add_patch(Polygon([[0, 0], [7.6, 0], [14, 8], [10.5, 8]], color="#CAD8EA", alpha=0.75))
    for i in range(8):
        ax.plot([0.4 + i * 0.25, 13.6], [5.1 + i * 0.22, 7.6 - i * 0.08], color="#B9C7D8", lw=0.7, alpha=0.45)
    draw_plane(ax, 8.2, 4.75, 1.22)
    ax.text(0.75, 6.95, SCHOOL, fontsize=13, color=BLUE, weight="bold")
    ax.text(0.75, 6.45, "Rapport de stage PFE - Data Analyst", fontsize=18, color=BLUE, weight="bold")
    ax.text(0.75, 5.55, TITLE, fontsize=16, color=DARK, weight="bold", wrap=True)
    ax.text(0.75, 2.25, f"Auteur : {AUTHOR}", fontsize=12.5, color=DARK)
    ax.text(0.75, 1.85, f"Encadrant pédagogique : {SUPERVISOR}", fontsize=12.5, color=DARK)
    ax.text(0.75, 1.45, f"Entreprise : {COMPANY}", fontsize=12.5, color=DARK)
    ax.text(0.75, 1.05, YEAR, fontsize=12.5, color=DARK)
    ax.add_patch(Rectangle((0.75, 0.62), 4.2, 0.08, color=BLUE2))
    return save(fig, path)


def create_industrial_visuals() -> list[Path]:
    paths = []
    # Site industriel aéronautique stylisé.
    fig, ax = canvas_base(ASSETS_DIR / "illustration_site_industriel.png", "Vue industrielle aéronautique", "Illustration corporate inspirée d'un environnement de production aéronautique")
    ax.add_patch(Rectangle((0, 0), 14, 7.25, color="#EAF0F7"))
    ax.add_patch(Rectangle((1.0, 1.0), 12.0, 3.1, color="#D8E0EA", ec=BLUE, lw=1.2))
    for i in range(8):
        ax.add_patch(Rectangle((1.4 + i * 1.3, 2.45), 0.8, 0.85, color="#FFFFFF", ec="#AAB7C7"))
    ax.add_patch(Rectangle((2.2, 4.1), 8.2, 0.55, color="#BCC8D8"))
    ax.add_patch(Rectangle((10.7, 1.0), 1.2, 4.4, color="#CBD5E1", ec=BLUE))
    ax.plot([0.5, 13.5], [0.8, 0.8], color=GREY, lw=2)
    draw_plane(ax, 7.1, 5.55, 0.75)
    paths.append(save(fig, ASSETS_DIR / "illustration_site_industriel.png"))

    # Atelier aéronautique.
    fig, ax = canvas_base(ASSETS_DIR / "illustration_usine_aeronautique.png", "Atelier de production aéronautique", "Assemblage, contrôle qualité et suivi des flux")
    for i in range(6):
        ax.add_patch(Rectangle((0.8 + i * 2.1, 1.0), 1.4, 4.9, color="#FDFEFF", ec="#C7D2E0"))
        ax.add_patch(Rectangle((0.95 + i * 2.1, 1.2), 1.1, 0.28, color=BLUE2))
    ax.add_patch(FancyBboxPatch((3.2, 3.5), 7.3, 0.65, boxstyle="round,pad=0.04,rounding_size=0.22", facecolor=BLUE, edgecolor="none"))
    ax.add_patch(Polygon([[4.8, 3.9], [6.4, 5.6], [5.8, 3.95]], color=BLUE2))
    ax.add_patch(Polygon([[7.7, 3.65], [9.5, 2.2], [8.2, 3.55]], color=BLUE2))
    ax.add_patch(Rectangle((2.2, 0.75), 9.6, 0.25, color="#AAB7C7"))
    paths.append(save(fig, ASSETS_DIR / "illustration_usine_aeronautique.png"))
    return paths


def create_flow_diagram(filename: str, title: str, steps: list[tuple[str, str]], subtitle: str = "") -> Path:
    fig, ax = canvas_base(ASSETS_DIR / filename, title, subtitle)
    x0, gap, w, h = 0.55, 0.45, (12.8 - 0.45 * (len(steps) - 1)) / len(steps), 2.1
    for i, (name, desc) in enumerate(steps):
        x = x0 + i * (w + gap)
        y = 3.0 if i % 2 == 0 else 2.25
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.10", facecolor="white", edgecolor=BLUE, lw=1.5))
        ax.add_patch(Circle((x + 0.28, y + h - 0.30), 0.17, color=BLUE2))
        ax.text(x + 0.28, y + h - 0.30, str(i + 1), ha="center", va="center", color="white", fontsize=8, weight="bold")
        ax.text(x + 0.55, y + h - 0.32, name, color=BLUE, fontsize=10.5, weight="bold", va="center")
        ax.text(x + 0.18, y + 0.85, desc, color=DARK, fontsize=8.3, va="center")
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + w + 0.37, y + 1.05), xytext=(x + w + 0.05, y + 1.05), arrowprops=dict(arrowstyle="->", lw=2, color=BLUE2))
    return save(fig, ASSETS_DIR / filename)


def create_screenshot(filename: str, title: str, lines: list[str], accent: str = BLUE2) -> Path:
    fig, ax = canvas_base(ASSETS_DIR / filename, title, "Capture générée automatiquement pour documenter le livrable technique")
    ax.add_patch(FancyBboxPatch((0.8, 1.0), 12.4, 5.6, boxstyle="round,pad=0.04,rounding_size=0.08", facecolor="#111827", edgecolor="#94A3B8", lw=1.2))
    ax.add_patch(Rectangle((0.8, 6.15), 12.4, 0.45, color="#1F2937"))
    for i, c in enumerate(["#EF4444", "#F59E0B", "#22C55E"]):
        ax.add_patch(Circle((1.1 + i * 0.25, 6.38), 0.07, color=c))
    y = 5.78
    for i, line in enumerate(lines[:18]):
        color = "#93C5FD" if line.strip().startswith(("import", "SELECT", "python", "df", "st.")) else "#E5E7EB"
        if line.strip().startswith(("#", "--")):
            color = "#A7F3D0"
        ax.text(1.05, y - i * 0.26, line, fontfamily="monospace", fontsize=7.8, color=color, va="top")
    ax.add_patch(Rectangle((0.8, 0.75), 12.4, 0.09, color=accent))
    return save(fig, ASSETS_DIR / filename)


def create_powerbi_mock(df: pd.DataFrame, kpi: pd.DataFrame) -> Path:
    fig, ax = canvas_base(ASSETS_DIR / "capture_powerbi_reporting.png", "Prototype Power BI - reporting industriel", "Vue de pilotage métier inspirée d'un rapport opérationnel")
    ax.add_patch(Rectangle((0.55, 1.0), 2.1, 5.8, color="#1E293B"))
    for y, lab in [(6.25, "Site"), (5.55, "Ligne"), (4.85, "Mois"), (4.15, "Anomalie")]:
        ax.text(0.78, y, lab, color="white", fontsize=9, weight="bold")
        ax.add_patch(Rectangle((0.78, y - 0.42), 1.55, 0.27, color="white"))
    cards = [("Conformité", fmt_pct(kpi.loc[0, "taux_conformite"])), ("Retard", fmt_pct(kpi.loc[0, "taux_retard_livraison"])), ("Volume", fmt_num(kpi.loc[0, "volume_total_produit"])), ("Coût", f"{kpi.loc[0, 'cout_total_non_qualite']/1_000_000:.1f} M€")]
    for i, (t, v) in enumerate(cards):
        x = 3.05 + i * 2.45
        ax.add_patch(FancyBboxPatch((x, 5.8), 2.05, 0.8, boxstyle="round,pad=0.05,rounding_size=0.07", facecolor="white", edgecolor="#CBD5E1"))
        ax.text(x + 0.15, 6.32, t, color=GREY, fontsize=8.5)
        ax.text(x + 0.15, 5.98, v, color=BLUE, fontsize=13, weight="bold")
    monthly = df.groupby("annee_mois").agg(qp=("quantite_produite", "sum"), qc=("quantite_conforme", "sum")).reset_index()
    monthly["tc"] = monthly["qc"] / monthly["qp"]
    ax1 = fig.add_axes([0.25, 0.34, 0.33, 0.26])
    ax1.plot(monthly["annee_mois"], monthly["tc"], marker="o", color=BLUE2, lw=2)
    ax1.set_title("Conformité mensuelle", fontsize=9)
    ax1.tick_params(axis="x", labelrotation=45, labelsize=6)
    ax1.tick_params(axis="y", labelsize=7)
    ax2 = fig.add_axes([0.63, 0.34, 0.25, 0.26])
    volumes = df.groupby("ligne_production")["quantite_produite"].sum().sort_values()
    ax2.barh(volumes.index, volumes.values, color=BLUE2)
    ax2.set_title("Volume par ligne", fontsize=9)
    ax2.tick_params(axis="both", labelsize=6)
    return save(fig, ASSETS_DIR / "capture_powerbi_reporting.png")


def create_assets(df: pd.DataFrame, kpi: pd.DataFrame) -> None:
    create_cover()
    create_industrial_visuals()
    create_flow_diagram(
        "architecture_globale_projet.png",
        "Architecture globale du projet",
        [("Data", "CSV industriel\nraw / processed"), ("Python", "nettoyage\nfeatures KPI"), ("Analyses", "notebooks\nEDA"), ("Reporting", "figures\nPDF Markdown"), ("Pilotage", "Streamlit\nPower BI cible")],
        "Organisation technique du dépôt portfolio",
    )
    create_flow_diagram(
        "pipeline_etl_industriel.png",
        "Pipeline ETL industriel",
        [("Extraction", "ordres\nqualité\nmachines"), ("Contrôle", "types\ndoublons\nmanquants"), ("Transformation", "variables\nretards\ncoûts"), ("Agrégation", "KPI ligne\nmois\nanomalie"), ("Restitution", "dashboard\nrapport\nalertes")],
        "Cycle de traitement des données de production",
    )
    create_flow_diagram(
        "workflow_analytique_industriel.png",
        "Workflow analytique industriel",
        [("Comprendre", "besoin métier\ncontraintes terrain"), ("Explorer", "descriptif\nqualité données"), ("Mesurer", "KPI\nécarts"), ("Interpréter", "causes\npriorités"), ("Recommander", "actions\nsuivi")],
        "Démarche Data Analyst orientée décision",
    )
    create_flow_diagram(
        "architecture_dashboard.png",
        "Architecture dashboard",
        [("Filtres", "date\nsite\nligne"), ("KPI cards", "qualité\ndélai\ncoût"), ("Graphiques", "évolution\ncomparaison"), ("Table critique", "OF\nanomalies\nimpact"), ("Décision", "priorités\nplans action")],
        "Organisation fonctionnelle de l'interface Streamlit",
    )
    create_flow_diagram(
        "schema_flux_donnees.png",
        "Schéma des flux de données",
        [("Production", "ordre\nvolume\ncycle"), ("Qualité", "conformité\nanomalies"), ("Machine", "température\nvibration"), ("Modèle data", "jointure\nstandardisation"), ("Pilotage", "KPI\nalerte")],
        "Flux métier depuis l'atelier jusqu'au reporting",
    )
    create_flow_diagram(
        "roadmap_amelioration_future.png",
        "Roadmap d'amélioration future",
        [("MVP", "reporting\nKPI"), ("Automatisation", "pipeline\nplanifié"), ("Alerting", "seuils\nnotifications"), ("ML", "détection\nanomalies"), ("IA industrielle", "prédiction\noptimisation")],
        "Perspectives Data Science et industrie 4.0",
    )
    create_screenshot("capture_execution_code.png", "Capture d'exécution Python", ["python src/data_generation.py", "Dataset généré : data/raw/donnees_production_airbus_atlantic.csv (12 000 lignes)", "python src/data_cleaning.py", "Données nettoyées : data/processed/donnees_production_nettoyees.csv", "python src/kpi_analysis.py", "KPI générés dans data/processed/", "python src/visualizations.py", "Visualisations générées : reports/figures/"])
    create_screenshot("capture_sql_reporting.png", "Capture SQL - extraction industrielle", ["-- Extraction des KPI de production par ligne", "SELECT", "  ligne_production,", "  SUM(quantite_produite) AS volume_total,", "  SUM(quantite_conforme) / SUM(quantite_produite) AS taux_conformite,", "  AVG(CASE WHEN delai_reel_jours > delai_prevu_jours THEN 1 ELSE 0 END) AS taux_retard,", "  SUM(cout_non_qualite) AS cout_non_qualite", "FROM production_orders", "WHERE date_production BETWEEN '2024-01-01' AND '2025-12-31'", "GROUP BY ligne_production", "ORDER BY cout_non_qualite DESC;"], "#60A5FA")
    create_screenshot("capture_notebook_eda.png", "Capture notebook - analyse exploratoire", ["import pandas as pd", "import plotly.express as px", "df = pd.read_csv('data/processed/donnees_production_nettoyees.csv')", "df.describe().T", "df.isna().sum().sort_values(ascending=False)", "fig = px.line(mensuel, x='annee_mois', y='taux_conformite')", "fig.show()", "# Interprétation : suivi mensuel de la stabilité qualité"], "#34D399")
    create_screenshot("capture_streamlit_code.png", "Capture Streamlit - dashboard", ["import streamlit as st", "df = charger_donnees()", "sites = st.multiselect('Site', sorted(df['site'].unique()))", "st.metric('Taux de conformité', formatter_pourcentage(taux_conformite))", "st.plotly_chart(fig_conformite, use_container_width=True)", "st.dataframe(anomalies_critiques, use_container_width=True)", "# Interface interactive pour le pilotage opérationnel"], "#38BDF8")
    create_powerbi_mock(df, kpi)


def markdown_report(df: pd.DataFrame, kpi: pd.DataFrame, lines: pd.DataFrame, anomalies: pd.DataFrame) -> str:
    figures = "\n".join([f"![{p.stem.replace('_', ' ').title()}](figures/{p.name})" for p in sorted(FIGURES_DIR.glob("*.png"))])
    assets = [
        "illustration_site_industriel.png",
        "illustration_usine_aeronautique.png",
        "architecture_globale_projet.png",
        "pipeline_etl_industriel.png",
        "workflow_analytique_industriel.png",
        "schema_flux_donnees.png",
        "architecture_dashboard.png",
        "roadmap_amelioration_future.png",
        "capture_execution_code.png",
        "capture_sql_reporting.png",
        "capture_notebook_eda.png",
        "capture_powerbi_reporting.png",
        "capture_dashboard_streamlit.png",
        "capture_streamlit_code.png",
    ]
    assets_md = "\n\n".join([f"![{Path(a).stem.replace('_', ' ').title()}](assets/{a})" for a in assets])
    top_line_cost = lines.sort_values("cout_non_qualite", ascending=False).iloc[0]
    top_line_late = lines.sort_values("taux_retard_livraison", ascending=False).iloc[0]
    top_anomaly = anomalies.iloc[0]
    return f"""# {TITLE}

**Établissement :** {SCHOOL}  
**Encadrant pédagogique :** {SUPERVISOR}  
**Entreprise :** {COMPANY}  
**Auteur :** {AUTHOR}  
**{YEAR}**

![Page de garde](assets/couverture_premium_airbus_atlantic.png)

## Sommaire

1. Remerciements
2. Résumé du projet
3. Introduction générale
4. Problématique industrielle
5. Objectifs métier et techniques
6. Technologies utilisées
7. Collecte et présentation des données
8. Nettoyage et préparation
9. Analyse exploratoire
10. Création des KPI industriels
11. Automatisation du reporting
12. Analyse des anomalies
13. Visualisations et interprétations
14. Dashboard industriel
15. Recommandations business
16. Limites du projet
17. Perspectives IA industrielle
18. Annexes techniques

## 1. Remerciements

Je remercie {SUPERVISOR} pour son encadrement pédagogique, ses orientations méthodologiques et son accompagnement dans la structuration de ce travail de fin d'études. Je remercie également {SCHOOL} pour la qualité de la formation et pour les compétences acquises en Data Science, analyse statistique, visualisation et aide à la décision.

Je remercie les équipes opérationnelles associées au contexte industriel d'Airbus Atlantic Casablanca pour l'inspiration métier de ce projet : pilotage de la production, suivi qualité, analyse des retards et amélioration continue.

## 2. Résumé du projet

Ce rapport présente le développement d'une solution de pilotage industriel basée sur la Data Analytics. Le projet couvre la création d'un pipeline data complet, depuis la préparation des données jusqu'à la restitution sous forme de dashboard et de rapport automatisé.

Les données utilisées sont synthétiques afin de respecter la confidentialité industrielle, tout en reproduisant une structure crédible de données aéronautiques : ordres de fabrication, lignes de production, conformité, délais, anomalies, coûts de non-qualité et signaux machine.

| Indicateur | Valeur |
|---|---:|
| Ordres de fabrication | {fmt_num(len(df))} |
| Volume total produit | {fmt_num(kpi.loc[0, 'volume_total_produit'])} |
| Taux de conformité | {fmt_pct(kpi.loc[0, 'taux_conformite'])} |
| Taux de retard livraison | {fmt_pct(kpi.loc[0, 'taux_retard_livraison'])} |
| Coût total de non-qualité | {fmt_num(kpi.loc[0, 'cout_total_non_qualite'])} € |
| Anomalies critiques | {fmt_num(kpi.loc[0, 'anomalies_critiques'])} |

## 3. Introduction générale

Airbus Atlantic Casablanca s'inscrit dans un environnement industriel aéronautique où la qualité, la traçabilité, les délais et la maîtrise des flux sont essentiels. Dans ce type d'organisation, les données de production constituent un levier majeur pour comprendre les écarts, prioriser les actions et sécuriser la performance opérationnelle.

La Data Analytics permet de transformer des données brutes en indicateurs exploitables : taux de conformité, retard livraison, coût de non-qualité, productivité, anomalies critiques et disponibilité machine. Elle contribue aussi à la mise en place d'une culture de pilotage par les faits.

## 4. Problématique industrielle

**Comment exploiter les données industrielles afin d'améliorer le pilotage de la production, détecter les anomalies et optimiser les performances opérationnelles chez Airbus Atlantic Casablanca ?**

Cette problématique implique de structurer les données, fiabiliser les calculs, construire des KPI pertinents, automatiser les visualisations et produire des recommandations compréhensibles par les équipes métier.

## 5. Objectifs métier et techniques

- Automatiser le reporting de performance industrielle.
- Construire un référentiel KPI fiable et reproductible.
- Identifier les retards, anomalies et coûts de non-qualité.
- Fournir un dashboard interactif pour le pilotage.
- Documenter les analyses dans un rapport professionnel de niveau Master / ingénieur.

## 6. Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Pipeline, nettoyage, KPI, rapport |
| Pandas / NumPy | Analyse et transformation des données |
| SQL | Logique d'extraction et agrégation industrielle |
| Matplotlib / Plotly | Visualisations statiques et interactives |
| Streamlit | Dashboard opérationnel |
| Power BI | Référence de reporting métier |
| Markdown / PDF | Documentation portfolio et mémoire |

## 7. Collecte et présentation des données

Le dataset contient {fmt_num(len(df))} observations. Chaque ligne représente un ordre de fabrication avec des informations de production, qualité, délai, coût et signaux machine. Les variables couvrent le cycle industriel complet : production, contrôle qualité, livraison, non-conformité et disponibilité machine.

## 8. Nettoyage et préparation

Le nettoyage inclut la conversion des dates, le contrôle des doublons, l'imputation des valeurs manquantes, la cohérence des quantités et la création de variables dérivées : taux de conformité, taux de non-conformité, retard livraison, écart délai, productivité par heure et indicateurs d'anomalies statistiques.

## 9. Analyse exploratoire

L'analyse exploratoire étudie les statistiques descriptives, les valeurs manquantes, les distributions, les corrélations et les anomalies. Elle permet d'identifier les zones de risque et de préparer les indicateurs de pilotage.

## 10. Création des KPI industriels

La ligne générant le coût de non-qualité le plus élevé est **{top_line_cost['ligne_production']}** avec **{fmt_num(top_line_cost['cout_non_qualite'])} €**. La ligne avec le taux de retard le plus élevé est **{top_line_late['ligne_production']}** avec **{fmt_pct(top_line_late['taux_retard_livraison'])}**. L'anomalie la plus fréquente est **{top_anomaly['type_anomalie']}** avec **{fmt_num(top_anomaly['nombre_anomalies'])} occurrences**.

## 11. Automatisation du reporting

Le reporting est automatisé via des scripts Python indépendants : génération des données, nettoyage, calcul KPI, visualisation, dashboard et génération du rapport Markdown/PDF.

## 12. Analyse des anomalies

Les anomalies sont analysées par type, gravité, ligne de production et coût associé. Les anomalies critiques sont mises en avant dans le dashboard afin de faciliter une réaction rapide des équipes qualité et production.

## 13. Visualisations et interprétations

{figures}

## 14. Dashboard industriel

Le dashboard Streamlit propose des filtres par date, site et ligne de production, des cartes KPI, des graphiques interactifs, un tableau des anomalies critiques et des recommandations métier.

## 15. Recommandations business

- Réduire les anomalies critiques via un rituel qualité-production quotidien.
- Prioriser les lignes cumulant retards et coût de non-qualité.
- Déployer des seuils d'alerte sur conformité, retard et disponibilité machine.
- Exploiter les signaux température et vibration pour initier une logique de maintenance prédictive.
- Connecter le pipeline à une base SQL et à un reporting Power BI cible.

## 16. Limites du projet

Le dataset est synthétique et ne remplace pas une donnée industrielle réelle. Les coûts sont estimés, les dépendances métier sont simplifiées et les recommandations doivent être validées avec les équipes terrain avant déploiement.

## 17. Perspectives IA industrielle

Les perspectives incluent la détection automatique d'anomalies, la prévision des retards, la prédiction du coût de non-qualité, la maintenance prédictive avancée et l'intégration d'un système d'alerte industriel.

## 18. Annexes techniques

{assets_md}

### Structure du projet

```text
data/raw -> data/processed -> src -> reports/figures -> dashboard -> rapport PDF
```

### Extrait de code KPI

```python
taux_conformite = df["quantite_conforme"].sum() / df["quantite_produite"].sum()
taux_retard = df["retard_livraison"].mean()
cout_non_qualite = df["cout_non_qualite"].sum()
```
"""


class TOCDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in {"Heading1", "Heading2"}:
            text = flowable.getPlainText()
            key = f"k{abs(hash((text, self.page)))}"
            self.canv.bookmarkPage(key)
            self.notify("TOCEntry", (0 if flowable.style.name == "Heading1" else 1, text, self.page, key))


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle("CoverTitle", fontName="Helvetica-Bold", fontSize=20, leading=25, textColor=colors.HexColor(BLUE), alignment=TA_CENTER, spaceAfter=10))
    s.add(ParagraphStyle("CoverMeta", fontName="Helvetica", fontSize=11, leading=15, textColor=colors.HexColor(DARK), alignment=TA_CENTER, spaceAfter=6))
    s["Heading1"].fontName = "Helvetica-Bold"
    s["Heading1"].fontSize = 15
    s["Heading1"].leading = 19
    s["Heading1"].textColor = colors.HexColor(BLUE)
    s["Heading1"].spaceBefore = 12
    s["Heading1"].spaceAfter = 7
    s["Heading2"].fontName = "Helvetica-Bold"
    s["Heading2"].fontSize = 11
    s["Heading2"].textColor = colors.HexColor(BLUE)
    s["BodyText"].fontSize = 9.2
    s["BodyText"].leading = 13
    s["BodyText"].alignment = TA_JUSTIFY
    s["BodyText"].spaceAfter = 6
    return s


def clean(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")


def para(text: str, style) -> Paragraph:
    return Paragraph(clean(text), style)


def img(path: Path, width: float) -> Image:
    im = Image(str(path))
    ratio = im.imageHeight / im.imageWidth
    im.drawWidth = width
    im.drawHeight = width * ratio
    return im


def make_table(rows: list[list[str]], widths: list[float]) -> Table:
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(BLUE)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(colors.HexColor(BLUE))
    canvas.rect(0, h - 0.55 * cm, w, 0.55 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.45 * cm, h - 0.36 * cm, "FST Mohammedia | Airbus Atlantic Casablanca | Data Analytics industrielle")
    canvas.setFillColor(colors.HexColor(GREY))
    canvas.drawRightString(w - 1.45 * cm, 0.75 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(df: pd.DataFrame, kpi: pd.DataFrame, lines: pd.DataFrame, anomalies: pd.DataFrame) -> None:
    st = styles()
    doc = TOCDoc(str(PDF_PATH), pagesize=A4, leftMargin=1.35 * cm, rightMargin=1.35 * cm, topMargin=1.5 * cm, bottomMargin=1.25 * cm)
    story = []
    story += [
        Spacer(1, 0.8 * cm),
        img(ASSETS_DIR / "couverture_premium_airbus_atlantic.png", 17.2 * cm),
        Spacer(1, 0.35 * cm),
        para(TITLE, st["CoverTitle"]),
        para(f"{SCHOOL}<br/>{COMPANY}<br/>Encadrant pédagogique : {SUPERVISOR}<br/>Auteur : {AUTHOR}<br/>{YEAR}", st["CoverMeta"]),
        PageBreak(),
    ]
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("toc1", fontName="Helvetica-Bold", fontSize=10, leftIndent=8, firstLineIndent=-8, leading=13, spaceBefore=4),
        ParagraphStyle("toc2", fontName="Helvetica", fontSize=9, leftIndent=22, firstLineIndent=-8, leading=11),
    ]
    story += [para("Table des matières", st["Heading1"]), toc, PageBreak()]

    kpi_rows = [["KPI", "Valeur"], ["Ordres de fabrication", fmt_num(len(df))], ["Volume produit", fmt_num(kpi.loc[0, "volume_total_produit"])], ["Taux de conformité", fmt_pct(kpi.loc[0, "taux_conformite"])], ["Taux de retard", fmt_pct(kpi.loc[0, "taux_retard_livraison"])], ["Coût non-qualité", f"{fmt_num(kpi.loc[0, 'cout_total_non_qualite'])} €"], ["Anomalies critiques", fmt_num(kpi.loc[0, "anomalies_critiques"])]]

    sections = [
        ("1. Remerciements", f"Je remercie {SUPERVISOR} pour son encadrement pédagogique et {SCHOOL} pour le cadre académique de ce projet. Je remercie également les équipes opérationnelles associées au contexte Airbus Atlantic Casablanca pour l'inspiration métier autour du pilotage industriel, de la qualité et de l'amélioration continue."),
        ("2. Résumé du projet", "Ce rapport présente une solution complète de pilotage et d'analyse de performance industrielle basée sur la Data Analytics. Le projet couvre la collecte, le nettoyage, l'analyse exploratoire, la création des KPI, l'automatisation du reporting, l'analyse des anomalies et la restitution dans un dashboard interactif."),
        ("3. Introduction générale", "Dans l'industrie aéronautique, la performance opérationnelle dépend de la maîtrise des délais, de la qualité, de la disponibilité machine et de la capacité à détecter rapidement les anomalies. La Data Analytics permet de transformer les données de production en leviers de décision mesurables."),
        ("4. Problématique industrielle", "Comment exploiter les données industrielles afin d'améliorer le pilotage de la production, détecter les anomalies et optimiser les performances opérationnelles chez Airbus Atlantic Casablanca ?"),
        ("5. Objectifs métier et techniques", "Les objectifs sont l'automatisation du reporting, la construction d'indicateurs fiables, l'analyse des anomalies, l'aide à la décision et la production d'un dashboard utilisable par les équipes métier."),
    ]
    for title, body in sections:
        story += [para(title, st["Heading1"]), para(body, st["BodyText"])]
        if title.startswith("2."):
            story += [make_table(kpi_rows, [8.2 * cm, 5.0 * cm]), Spacer(1, 0.2 * cm)]

    story += [
        para("6. Technologies utilisées", st["Heading1"]),
        make_table([["Technologie", "Utilisation"], ["Python", "Pipeline, nettoyage, KPI et rapport"], ["Pandas / NumPy", "Transformation et agrégation"], ["SQL", "Extraction et requêtes analytiques"], ["Power BI", "Reporting métier cible"], ["Streamlit", "Dashboard interactif"], ["Matplotlib / Plotly", "Visualisations KPI"]], [4.2 * cm, 10.5 * cm]),
        para("7. Collecte et présentation des données", st["Heading1"]),
        para(f"Le dataset contient {fmt_num(len(df))} ordres de fabrication et {fmt_num(kpi.loc[0, 'volume_total_produit'])} pièces produites. Les données sont synthétiques pour respecter la confidentialité industrielle, mais elles reproduisent une structure réaliste de suivi de production aéronautique.", st["BodyText"]),
        img(ASSETS_DIR / "illustration_site_industriel.png", 15.5 * cm),
        para("8. Nettoyage et préparation", st["Heading1"]),
        para("La préparation comprend la conversion des dates, le contrôle des doublons, le traitement des valeurs manquantes, la création des variables de retard, conformité, productivité, écart de délai et indicateurs d'anomalies statistiques.", st["BodyText"]),
        img(ASSETS_DIR / "pipeline_etl_industriel.png", 15.5 * cm),
        para("9. Analyse exploratoire", st["Heading1"]),
        para("L'analyse exploratoire étudie les distributions, corrélations, valeurs manquantes et anomalies statistiques. Elle permet de détecter les lignes sensibles et les familles d'anomalies les plus coûteuses.", st["BodyText"]),
        img(ASSETS_DIR / "capture_notebook_eda.png", 15.5 * cm),
        para("10. Création des KPI industriels", st["Heading1"]),
        para("Les KPI industriels couvrent la conformité, la non-conformité, les retards, la productivité, le coût de non-qualité, la disponibilité machine, les anomalies par type et les anomalies critiques.", st["BodyText"]),
    ]
    line_rows = [["Ligne", "Conformité", "Retard", "Coût non-qualité"]]
    for _, r in lines.sort_values("cout_non_qualite", ascending=False).iterrows():
        line_rows.append([str(r["ligne_production"]), fmt_pct(r["taux_conformite"]), fmt_pct(r["taux_retard_livraison"]), f"{fmt_num(r['cout_non_qualite'])} €"])
    story += [make_table(line_rows, [5.0 * cm, 3.0 * cm, 3.0 * cm, 4.0 * cm])]

    media_sections = [
        ("11. Automatisation du reporting", "capture_execution_code.png", "Le pipeline est automatisé par scripts Python afin de rendre l'analyse reproductible dans VS Code et exploitable dans un portfolio GitHub."),
        ("12. Analyse SQL et préparation métier", "capture_sql_reporting.png", "La logique SQL permet de formaliser les agrégations industrielles attendues dans un environnement de production réel."),
        ("13. Dashboard Power BI cible", "capture_powerbi_reporting.png", "La maquette Power BI illustre la logique de reporting métier attendue pour un comité de pilotage opérationnel."),
        ("14. Dashboard Streamlit", "capture_dashboard_streamlit.png", "Le dashboard Streamlit offre un pilotage interactif avec filtres, cartes KPI, visualisations et tableau des anomalies critiques."),
        ("15. Architecture dashboard", "architecture_dashboard.png", "L'architecture de l'interface organise les filtres, KPI cards, graphiques, tables critiques et recommandations métier."),
    ]
    for title, asset, body in media_sections:
        story += [para(title, st["Heading1"]), para(body, st["BodyText"]), img(ASSETS_DIR / asset, 15.5 * cm)]

    story += [para("16. Visualisations et interprétations", st["Heading1"])]
    for fig_path in sorted(FIGURES_DIR.glob("*.png")):
        story += [para(fig_path.stem.replace("_", " ").title(), st["Heading2"]), img(fig_path, 15.2 * cm)]

    final_assets = [
        ("17. Recommandations business", "workflow_analytique_industriel.png", "Prioriser les anomalies critiques, surveiller les lignes à fort retard, automatiser les seuils d'alerte et engager une démarche de maintenance prédictive basée sur les signaux machine."),
        ("18. Limites du projet", "schema_flux_donnees.png", "Les données sont synthétiques, les coûts restent estimatifs et les recommandations doivent être validées par les équipes terrain avant généralisation."),
        ("19. Perspectives IA industrielle", "roadmap_amelioration_future.png", "Les perspectives incluent la détection automatique d'anomalies, la prédiction des retards, la maintenance prédictive avancée et l'intégration avec une base SQL industrielle."),
        ("20. Annexes techniques", "architecture_globale_projet.png", "Le dépôt regroupe les données, notebooks, scripts, figures, dashboard et rapports Markdown/PDF."),
    ]
    for title, asset, body in final_assets:
        story += [para(title, st["Heading1"]), para(body, st["BodyText"]), img(ASSETS_DIR / asset, 15.5 * cm)]

    code = dedent("""\
    taux_conformite = df["quantite_conforme"].sum() / df["quantite_produite"].sum()
    taux_retard = df["retard_livraison"].mean()
    cout_non_qualite = df["cout_non_qualite"].sum()
    """)
    story += [para("Extrait de code KPI", st["Heading2"]), Paragraph(f"<font name='Courier' size='8'>{clean(code)}</font>", st["BodyText"]), img(ASSETS_DIR / "capture_streamlit_code.png", 15.5 * cm)]
    doc.multiBuild(story, onFirstPage=header_footer, onLaterPages=header_footer)


def main() -> None:
    df, kpi, lines, anomalies = load_data()
    create_assets(df, kpi)
    MD_PATH.write_text(markdown_report(df, kpi, lines, anomalies), encoding="utf-8")
    build_pdf(df, kpi, lines, anomalies)
    copyfile(PDF_PATH, ROOT_PDF_PATH)
    root_md = MD_PATH.read_text(encoding="utf-8").replace("](assets/", "](reports/assets/").replace("](figures/", "](reports/figures/")
    ROOT_MD_PATH.write_text(root_md, encoding="utf-8")
    print(f"Markdown généré : {MD_PATH}")
    print(f"PDF généré : {PDF_PATH}")
    print(f"Copies racine : {ROOT_MD_PATH} et {ROOT_PDF_PATH}")


if __name__ == "__main__":
    main()
