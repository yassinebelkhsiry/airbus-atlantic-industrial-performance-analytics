# Rapport de synthèse - Performance industrielle Airbus Atlantic

## Contexte

Ce rapport présente une analyse de performance industrielle appliquée à un environnement aéronautique. Le projet couvre la génération d'un jeu de données confidentiel simulé, le nettoyage, le calcul des KPI, la visualisation et la restitution opérationnelle via un dashboard Streamlit.

## Périmètre d'analyse

- Sites industriels : Casablanca, Rochefort, Montoir-de-Bretagne
- Lignes de production : programmes A320, A330, A350, assemblage cabine et composite
- Horizon temporel : janvier 2024 à décembre 2025
- Indicateurs : conformité, non-conformité, retards, productivité, coûts qualité, disponibilité machine et anomalies critiques

## Résultats clés

- Le dataset contient 12 000 ordres de fabrication et 755 839 pièces produites.
- Le taux de conformité global est de 94,7 %, pour un taux de non-conformité de 5,3 %.
- Le taux de retard livraison atteint 35,0 %, avec une criticité plus forte sur la Ligne Composite.
- Le coût total de non-qualité est estimé à 16,8 M€ sur la période étudiée.
- La Ligne A350 est le principal contributeur au coût de non-qualité.
- Les défauts dimensionnels, les défauts d'assemblage et les retouches peinture constituent les principales familles d'anomalies.

## Recommandations métier

1. Mettre en place un rituel quotidien qualité-production sur les anomalies critiques.
2. Surveiller les lignes présentant simultanément un taux de retard élevé et une disponibilité machine faible.
3. Industrialiser un reporting mensuel automatisé avec extraction, nettoyage, calcul KPI et diffusion dashboard.
4. Définir des seuils d'alerte sur le taux de conformité, le coût de non-qualité et les signaux machine.
5. Prioriser les analyses causes racines sur les types d'anomalies les plus coûteux.

## Visualisations disponibles

Les figures générées automatiquement sont disponibles dans `reports/figures/` :

- `evolution_mensuelle_taux_conformite.png`
- `volume_produit_par_ligne.png`
- `top_anomalies.png`
- `cout_non_qualite_par_mois.png`
- `retards_par_ligne_production.png`
- `heatmap_correlation.png`
- `distribution_temps_cycle.png`
