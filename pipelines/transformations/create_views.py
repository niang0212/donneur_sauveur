from google.cloud import bigquery

PROJECT_ID = "donneursauveur-486312"
DATASET_ID = "donneur_sauveur"

client = bigquery.Client(project=PROJECT_ID)

VIEWS = {
    "v_donneurs_eligibles": """
        SELECT
          id_donneur,
          nom_complet,
          groupe_sanguin,
          tel,
          region,
          adresse,
          latitude,
          longitude,
          date_dernier_don,
          DATE_DIFF(CURRENT_DATE(), date_dernier_don, DAY) AS jours_depuis_dernier_don
        FROM donneur_sauveur.raw_donors
        WHERE DATE_DIFF(CURRENT_DATE(), date_dernier_don, DAY) >= 90
    """,

    "v_eligibles_par_groupe": """
        SELECT
          groupe_sanguin,
          COUNT(*) AS nb_donneurs_eligibles
        FROM donneur_sauveur.v_donneurs_eligibles
        GROUP BY groupe_sanguin
    """,

    "v_disponibilite_region_groupe": """
        SELECT
          region,
          groupe_sanguin,
          COUNT(*) AS nb_donneurs_eligibles
        FROM donneur_sauveur.v_donneurs_eligibles
        GROUP BY region, groupe_sanguin
    """,

    "v_regions_en_deficit": """
        SELECT
          region,
          groupe_sanguin,
          nb_donneurs_eligibles
        FROM donneur_sauveur.v_disponibilite_region_groupe
        WHERE nb_donneurs_eligibles < 50
    """,

   "v_centre": """
        SELECT
          id_centre,
          nom,
          region,
          latitude,
          longitude
        FROM donneur_sauveur.raw_centers
    """,
    "v_donations": """
        SELECT
          id_don,
          id_donneur,
          id_centre, 
          date_don
        FROM donneur_sauveur.raw_donations
    """
}

for view_name, query in VIEWS.items():
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{view_name}"
    view = bigquery.Table(table_id)
    view.view_query = query
    view = client.create_table(view, exists_ok=True)
    print(f"Vue {view_name} créée ou mise à jour.")
