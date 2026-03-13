#!/bin/bash
set -e

echo "======================================"
echo "🚀 PIPELINE DONNEUR-SAUVEUR"
echo "======================================"

echo ""
echo "1️⃣ Génération des données simulées"
python pipelines/ingestion/generate_data.py

echo ""
echo "2️⃣ Chargement des données dans BigQuery"
python pipelines/ingestion/load_bigquery.py

echo ""
echo "3️⃣ Création / mise à jour des vues analytiques"
python pipelines/transformations/create_views.py

echo ""
echo "4️⃣ Contrôles de qualité des données"
python pipelines/quality/run_quality_checks.py

echo ""
echo "======================================"
echo "✅ PIPELINE TERMINÉ AVEC SUCCÈS"
echo "======================================"