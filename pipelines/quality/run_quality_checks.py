from google.cloud import bigquery

PROJECT_ID = "donneursauveur-486312"
DATASET_ID = "donneur_sauveur"

client = bigquery.Client(project=PROJECT_ID)

checks = {
    "donneurs_incomplets": """
        SELECT COUNT(*) AS nb
        FROM donneur_sauveur.raw_donors
        WHERE
          id_donneur IS NULL
          OR groupe_sanguin IS NULL
          OR region IS NULL
          OR date_dernier_don IS NULL
    """,

    "groupes_sanguins_invalides": """
        SELECT COUNT(*) AS nb
        FROM donneur_sauveur.raw_donors
        WHERE groupe_sanguin NOT IN ('A+','A-','B+','B-','AB+','AB-','O+','O-')
    """,

    "coordonnees_invalides": """
        SELECT COUNT(*) AS nb
        FROM donneur_sauveur.raw_donors
        WHERE
          latitude NOT BETWEEN 12 AND 17
          OR longitude NOT BETWEEN -18 AND -11
    """,

    "dons_orphelins": """
        SELECT COUNT(*) AS nb
        FROM donneur_sauveur.raw_donations d
        LEFT JOIN donneur_sauveur.raw_donors r
          ON d.id_donneur = r.id_donneur
        LEFT JOIN donneur_sauveur.raw_centers c
          ON d.id_centre = c.id_centre
        WHERE r.id_donneur IS NULL OR c.id_centre IS NULL
    """,

    "doublons_donneurs": """
        SELECT COUNT(*) AS nb
        FROM (
            SELECT id_donneur
            FROM donneur_sauveur.raw_donors
            GROUP BY id_donneur
            HAVING COUNT(*) > 1
        )
    """
}

print("=== CONTRÔLES DE QUALITÉ DES DONNÉES ===")

critical_errors = 0

for check_name, query in checks.items():
    job = client.query(query)
    result = list(job.result())[0].nb

    print(f"{check_name} : {result}")

    if result > 0:
        critical_errors += 1

if critical_errors > 0:
    raise Exception(
        f"❌ {critical_errors} contrôles de qualité ont échoué. Arrêt du pipeline."
    )

print("✅ Tous les contrôles de qualité sont conformes.")
