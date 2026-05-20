# Airbus Atlantic Industrial Performance Analytics

![Couverture du projet](reports/assets/couverture_premium_airbus_atlantic.png)

<h3 align="center">
  Projet Data Analytics industriel - Airbus Atlantic Casablanca - Stage PFE 2023/2024
</h3>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-Data%20Analytics-173B6D?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-Dashboard-2F80ED?style=for-the-badge&logo=streamlit&logoColor=white">
  <img alt="Pandas" src="https://img.shields.io/badge/Pandas-KPI%20Analysis-5F6B7A?style=for-the-badge&logo=pandas&logoColor=white">
  <img alt="Licence" src="https://img.shields.io/badge/Licence-MIT-white?style=for-the-badge">
</p>

<p align="center">
  <a href="rapport_stage_airbus_atlantic.pdf"><b>Rapport PDF</b></a> ·
  <a href="dashboard/app_streamlit.py"><b>Dashboard Streamlit</b></a> ·
  <a href="reports/figures"><b>Visualisations KPI</b></a> ·
  <a href="src"><b>Code source</b></a>
</p>

Projet Data Analyst / Data Science consacré au **pilotage de la performance industrielle** et au **suivi des anomalies de production** dans un contexte aéronautique.

Le projet simule un cas professionnel de stage PFE chez **Airbus Atlantic Casablanca** : automatisation du reporting, analyse de données industrielles, création de KPI, visualisations avancées, dashboard Streamlit et rapport PDF prêt pour un portfolio GitHub.

> Les données sont synthétiques afin de respecter la confidentialité industrielle, tout en conservant une structure réaliste de données de production aéronautique.

## Aperçu Exécutif

![Synthèse KPI premium](reports/assets/synthese_kpi_premium.png)

| Indicateur | Résultat |
|---|---:|
| Ordres de fabrication analysés | **12 000** |
| Volume total produit | **755 839 pièces** |
| Taux de conformité global | **94,7 %** |
| Taux de non-conformité | **5,3 %** |
| Taux de retard livraison | **35,0 %** |
| Coût total de non-qualité | **16,8 M€** |
| Anomalies critiques | **1 769** |

## Démonstration Visuelle

### Dashboard et Reporting

<table>
  <tr>
    <td width="50%">
      <img src="reports/assets/capture_dashboard_streamlit.png" alt="Dashboard Streamlit">
      <br><b>Dashboard Streamlit interactif</b>
    </td>
    <td width="50%">
      <img src="reports/assets/capture_powerbi_reporting.png" alt="Prototype Power BI">
      <br><b>Prototype de reporting Power BI</b>
    </td>
  </tr>
</table>

### Synthèse Décisionnelle

<table>
  <tr>
    <td width="50%">
      <img src="reports/assets/synthese_kpi_premium.png" alt="Synthèse KPI premium">
      <br><b>Synthèse exécutive des KPI</b>
    </td>
    <td width="50%">
      <img src="reports/assets/matrice_priorisation_metier.png" alt="Matrice de priorisation métier">
      <br><b>Matrice de priorisation métier</b>
    </td>
  </tr>
</table>

### Architecture Data et Pipeline Industriel

<table>
  <tr>
    <td width="50%">
      <img src="reports/assets/architecture_globale_projet.png" alt="Architecture globale du projet">
      <br><b>Architecture globale du projet</b>
    </td>
    <td width="50%">
      <img src="reports/assets/pipeline_etl_industriel.png" alt="Pipeline ETL industriel">
      <br><b>Pipeline ETL industriel</b>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="reports/assets/workflow_analytique_industriel.png" alt="Workflow analytique industriel">
      <br><b>Workflow analytique industriel</b>
    </td>
    <td width="50%">
      <img src="reports/assets/schema_flux_donnees.png" alt="Schéma des flux de données">
      <br><b>Schéma des flux de données</b>
    </td>
  </tr>
</table>

### Environnement Aéronautique

<table>
  <tr>
    <td width="50%">
      <img src="reports/assets/illustration_site_industriel.png" alt="Site industriel aéronautique">
      <br><b>Vue industrielle aéronautique</b>
    </td>
    <td width="50%">
      <img src="reports/assets/illustration_usine_aeronautique.png" alt="Atelier de production aéronautique">
      <br><b>Atelier de production aéronautique</b>
    </td>
  </tr>
</table>

## Objectifs du Projet

- Automatiser le reporting de performance industrielle.
- Nettoyer et analyser plusieurs milliers de lignes de données de production.
- Construire des KPI opérationnels liés aux délais, volumes, anomalies et productivité.
- Identifier les écarts de performance par ligne, site et type de pièce.
- Détecter les anomalies statistiques et les anomalies critiques.
- Fournir un dashboard interactif pour le pilotage opérationnel.
- Produire un rapport PDF professionnel de niveau Master / ingénieur.

## Stack Technique

| Domaine | Outils |
|---|---|
| Data processing | Python, Pandas, NumPy |
| Analyse statistique | Pandas, SciPy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Dashboard | Streamlit |
| Reporting | Markdown, ReportLab, PDF |
| Portfolio | Git, GitHub |

## Architecture du Projet

```text
airbus-atlantic-industrial-performance-analytics/
├── README.md
├── LICENSE
├── requirements.txt
├── rapport_stage_airbus_atlantic.md
├── rapport_stage_airbus_atlantic.pdf
├── data/
│   ├── raw/
│   │   └── donnees_production_airbus_atlantic.csv
│   └── processed/
│       ├── donnees_production_nettoyees.csv
│       ├── kpi_globaux.csv
│       ├── kpi_lignes_production.csv
│       ├── kpi_mensuels.csv
│       └── kpi_anomalies.csv
├── notebooks/
│   ├── 01_exploration_donnees.ipynb
│   └── 02_analyse_kpi_industriels.ipynb
├── src/
│   ├── data_generation.py
│   ├── data_cleaning.py
│   ├── kpi_analysis.py
│   └── visualizations.py
├── reports/
│   ├── assets/
│   ├── figures/
│   ├── generate_stage_report.py
│   └── rapport_synthese.md
└── dashboard/
    └── app_streamlit.py
```

## Dataset

Le dataset contient plus de **10 000 lignes** et représente des ordres de fabrication industriels.

| Famille | Variables |
|---|---|
| Production | `date_production`, `site`, `ligne_production`, `type_piece`, `ordre_fabrication` |
| Volumes | `quantite_produite`, `quantite_conforme`, `quantite_non_conforme` |
| Délais | `delai_prevu_jours`, `delai_reel_jours`, `statut_livraison` |
| Qualité | `type_anomalie`, `gravite_anomalie`, `cout_non_qualite` |
| Organisation | `operateur_equipe`, `shift` |
| Machine | `taux_disponibilite_machine`, `temperature_machine`, `vibration_machine` |

## KPI Suivis

| KPI | Objectif métier |
|---|---|
| Taux de conformité | Mesurer la qualité globale de production |
| Taux de non-conformité | Identifier les pertes qualité |
| Taux de retard livraison | Suivre la tenue des délais |
| Productivité par ligne | Comparer la performance des lignes |
| Coût de non-qualité | Prioriser les actions correctives |
| Temps de cycle moyen | Surveiller l'efficacité industrielle |
| Disponibilité machine | Mesurer la stabilité des équipements |
| Anomalies par type | Identifier les causes fréquentes |
| Anomalies critiques | Suivre les incidents à fort impact |
| Performance mensuelle | Observer les tendances temporelles |

## Galerie des Visualisations KPI

<table>
  <tr>
    <td width="50%">
      <img src="reports/figures/evolution_mensuelle_taux_conformite.png" alt="Évolution mensuelle du taux de conformité">
      <br><b>Évolution mensuelle du taux de conformité</b>
    </td>
    <td width="50%">
      <img src="reports/figures/volume_produit_par_ligne.png" alt="Volume produit par ligne">
      <br><b>Volume produit par ligne</b>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="reports/figures/top_anomalies.png" alt="Top anomalies">
      <br><b>Top anomalies de production</b>
    </td>
    <td width="50%">
      <img src="reports/figures/cout_non_qualite_par_mois.png" alt="Coût de non-qualité par mois">
      <br><b>Coût de non-qualité par mois</b>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="reports/figures/retards_par_ligne_production.png" alt="Retards par ligne">
      <br><b>Retards par ligne de production</b>
    </td>
    <td width="50%">
      <img src="reports/figures/heatmap_correlation.png" alt="Heatmap de corrélation">
      <br><b>Heatmap de corrélation</b>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      <img src="reports/figures/distribution_temps_cycle.png" alt="Distribution des temps de cycle">
      <br><b>Distribution des temps de cycle</b>
    </td>
  </tr>
</table>

## Rapport de Stage PFE

Le projet inclut un rapport complet, structuré comme un mémoire de fin d'études Data Analyst en industrie aéronautique.

| Format | Fichier |
|---|---|
| PDF | [`rapport_stage_airbus_atlantic.pdf`](rapport_stage_airbus_atlantic.pdf) |
| Markdown | [`rapport_stage_airbus_atlantic.md`](rapport_stage_airbus_atlantic.md) |

Le rapport contient :

- page de garde premium ;
- année universitaire 2023/2024 ;
- problématique industrielle ;
- analyse exploratoire ;
- KPI industriels ;
- dashboard, schémas data et visualisations KPI ;
- visualisations et interprétations ;
- recommandations métier ;
- limites et perspectives IA industrielle.

## Résultats Clés

- Le taux de conformité global atteint **94,7 %**.
- Le taux de retard livraison atteint **35,0 %**, ce qui justifie un pilotage régulier par ligne.
- Le coût total de non-qualité est estimé à **16,8 M€** sur la période analysée.
- La **Ligne A350** concentre le coût de non-qualité le plus élevé.
- La **Ligne Composite** présente le taux de retard le plus important.
- Les anomalies les plus fréquentes sont les défauts dimensionnels, les défauts d'assemblage et les retouches peinture.

## Recommandations Métier

- Prioriser les plans d'action qualité sur les anomalies critiques.
- Mettre en place un suivi hebdomadaire des lignes cumulant retards, faible disponibilité machine et coût de non-qualité élevé.
- Automatiser la diffusion des KPI pour réduire le temps de préparation du reporting.
- Ajouter des seuils d'alerte sur le taux de conformité, les retards et les signaux machine.
- Exploiter les signaux température et vibration pour initier une logique de maintenance prédictive.

## Exécuter le Projet

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

python src/data_generation.py
python src/data_cleaning.py
python src/kpi_analysis.py
python src/visualizations.py

streamlit run dashboard/app_streamlit.py
```

## Régénérer le Rapport PDF

```bash
python reports/generate_stage_report.py
```

## Commandes GitHub

```bash
git init
git add .
git commit -m "Initial commit - Airbus Atlantic Industrial Performance Analytics"
git branch -M main
git remote add origin URL_DU_REPO
git push -u origin main
```

## Auteur

**Yassine BEL-KHSIRY**  
Master Data Science

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier [`LICENSE`](LICENSE) pour plus de détails.
