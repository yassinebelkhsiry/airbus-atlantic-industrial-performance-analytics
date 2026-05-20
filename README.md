# Airbus Atlantic Industrial Performance Analytics

Projet Data Analyst / Data Science consacré au pilotage de la performance industrielle et au suivi des anomalies de production dans un contexte aéronautique.

## Contexte métier

Dans le cadre d'un stage PFE en Data Analysis chez Airbus Atlantic à Casablanca, ce projet reproduit un cas d'usage professionnel de reporting industriel : consolidation de données de production, nettoyage, suivi d'indicateurs opérationnels, détection d'anomalies et restitution via un dashboard interactif.

Les données utilisées sont synthétiques afin de respecter la confidentialité industrielle. Elles ont été conçues pour représenter un environnement réaliste : ordres de fabrication, lignes de production, volumes, conformité, délais, anomalies qualité, coûts de non-qualité et signaux machine.

## Objectifs

- Automatiser le reporting de performance industrielle.
- Nettoyer et analyser plusieurs milliers de lignes de données de production.
- Construire des KPI opérationnels liés aux délais, volumes, anomalies et productivité.
- Identifier les écarts de performance par ligne, site et type de pièce.
- Produire des visualisations professionnelles adaptées à un portfolio GitHub.
- Mettre à disposition un dashboard Streamlit pour le pilotage opérationnel.

## Stack technique

- Python : pandas, numpy, scipy
- Visualisation : matplotlib, seaborn, plotly
- Dashboard : Streamlit
- Analyse : notebooks Jupyter
- Versioning : Git et GitHub

## Architecture du projet

```text
airbus-atlantic-industrial-performance-analytics/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_exploration_donnees.ipynb
│   └── 02_analyse_kpi_industriels.ipynb
├── src/
│   ├── data_generation.py
│   ├── data_cleaning.py
│   ├── kpi_analysis.py
│   └── visualizations.py
├── reports/
│   ├── figures/
│   └── rapport_synthese.md
└── dashboard/
    └── app_streamlit.py
```

## Dataset utilisé

Le dataset contient plus de 10 000 lignes et les colonnes suivantes :

- `date_production`, `site`, `ligne_production`, `type_piece`, `ordre_fabrication`
- `quantite_produite`, `quantite_conforme`, `quantite_non_conforme`
- `temps_cycle_min`, `delai_prevu_jours`, `delai_reel_jours`, `statut_livraison`
- `type_anomalie`, `gravite_anomalie`, `cout_non_qualite`
- `operateur_equipe`, `shift`
- `taux_disponibilite_machine`, `temperature_machine`, `vibration_machine`

## KPIs suivis

1. Taux de conformité
2. Taux de non-conformité
3. Taux de retard livraison
4. Productivité par ligne
5. Coût de non-qualité
6. Temps de cycle moyen
7. Disponibilité machine
8. Nombre d'anomalies par type
9. Anomalies critiques
10. Évolution mensuelle de la performance

## Visualisations

Les graphiques sont générés automatiquement dans `reports/figures/` :

![Évolution mensuelle du taux de conformité](reports/figures/evolution_mensuelle_taux_conformite.png)
![Volume produit par ligne](reports/figures/volume_produit_par_ligne.png)
![Top anomalies](reports/figures/top_anomalies.png)
![Coût de non-qualité par mois](reports/figures/cout_non_qualite_par_mois.png)
![Retards par ligne de production](reports/figures/retards_par_ligne_production.png)
![Heatmap de corrélation](reports/figures/heatmap_correlation.png)
![Distribution des temps de cycle](reports/figures/distribution_temps_cycle.png)

## Rapport de stage

Un rapport de stage complet, structuré comme un mémoire de fin d'études Data Analyst en industrie aéronautique, est disponible aux formats Markdown et PDF :

- `rapport_stage_airbus_atlantic.md`
- `rapport_stage_airbus_atlantic.pdf`

Le rapport contient une page de garde premium, une table des matières, les informations académiques FST Mohammedia, l'encadrant pédagogique, l'analyse exploratoire, les KPI industriels, les visualisations, des captures Python, SQL, Power BI et Streamlit, les recommandations métier, les limites, les perspectives IA industrielle et les annexes techniques.

## Résultats clés

- Le dataset généré contient **12 000 ordres de fabrication** et **755 839 pièces produites**.
- Le taux de conformité global atteint **94,7 %**, avec un taux de non-conformité de **5,3 %**.
- Le taux de retard livraison est de **35,0 %**, ce qui justifie un suivi régulier par ligne de production.
- Le coût total de non-qualité est estimé à **16,8 M€** sur la période analysée.
- La **Ligne A350** concentre le coût de non-qualité le plus élevé, tandis que la **Ligne Composite** présente le taux de retard le plus important.
- Les anomalies les plus fréquentes sont les défauts dimensionnels, les défauts d'assemblage et les retouches peinture.

## Recommandations métier

- Prioriser les plans d'action qualité sur les anomalies critiques et les familles d'anomalies les plus coûteuses.
- Mettre en place un suivi hebdomadaire des lignes cumulant retards, faible disponibilité machine et coût de non-qualité élevé.
- Automatiser la diffusion des KPI pour réduire le temps de préparation du reporting.
- Ajouter des seuils d'alerte sur le taux de conformité, les retards et les signaux machine.
- Croiser les analyses dashboard avec les retours des équipes opérationnelles pour valider les causes racines.

## Comment exécuter le projet

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
Master Data Science - Aix-Marseille Université
