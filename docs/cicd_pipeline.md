-----------------------------------Documentation CI/CD------------------------------------------------------------
Objectif
Le pipeline CI/CD du projet Donneur-Sauveur automatise l’exécution des différentes étapes du traitement des données afin de garantir la reproductibilité et la fiabilité du système.

Déclenchement du pipeline
Le pipeline est exécuté automatiquement dans deux cas :
-lorsqu’un nouveau commit est poussé sur la branche principale
-lorsqu’il est déclenché manuellement via GitHub Actions

Environnement d’exécution
Le pipeline s’exécute dans un environnement Linux fourni par GitHub Actions et utilise Docker afin de garantir la reproductibilité de l’environnement d’exécution.

Étapes du pipeline
Le pipeline exécute les étapes suivantes :
1 Génération des données simulées représentant les donneurs et les dons.
2 Chargement des données dans BigQuery.
3 Création et mise à jour des vues analytiques.
4 Exécution des contrôles de qualité des données.

Gestion des erreurs
Le pipeline utilise un mécanisme d’arrêt automatique (set -e) qui interrompt l’exécution dès qu’une erreur est détectée.

Sécurisation des credentials
Les credentials Google Cloud sont stockés dans GitHub Secrets sous forme encodée en base64 et injectés dynamiquement dans l’environnement d’exécution du pipeline.