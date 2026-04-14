import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

# ================================
# CONFIG
# ================================
PROJECT_ID = "donneursauveur-486312"
DATASET_ID = "donneur_sauveur"

credentials = service_account.Credentials.from_service_account_file(
    "secrets/sa-donneur-sauveur.json"
)

client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)

# ================================
# REGIONS
# ================================
REGIONS = {
    "Dakar": [("Dakar", 14.7167, -17.4677), ("Guédiawaye", 14.7833, -17.3833), ("Pikine", 14.75, -17.4)],
    "Thiès": [("Thiès", 14.79, -16.92), ("Mbour", 14.41, -16.96)],
    "Saint-Louis": [("Saint-Louis", 16.02, -16.5)],
    "Kaolack": [("Kaolack", 14.16, -16.08), ("Nioro du Rip", 13.75, -15.78)],
}

# ================================
# UI
# ================================
st.title("🩸 Donneur Sauveur - Interface de gestion")

menu = st.sidebar.selectbox("Menu", ["Donneur", "Centre", "Don"])

# ================================
# DONNEUR
# ================================
if menu == "Donneur":
    st.header("Ajouter un donneur")

    nom = st.text_input("Nom complet")
    groupe = st.selectbox("Groupe sanguin", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    tel = st.text_input("Téléphone")

    region = st.selectbox("Région", list(REGIONS.keys()))
    adresses = REGIONS[region]

    adresse_selectionnee = st.selectbox("Adresse", [a[0] for a in adresses])

    latitude, longitude = 0, 0
    for a in adresses:
        if a[0] == adresse_selectionnee:
            latitude, longitude = a[1], a[2]

    st.info(f"📍 Latitude: {latitude} | Longitude: {longitude}")

    numero_proche = st.text_input("Numéro proche")
    notes_sante = st.text_area("Notes santé")

    if st.button("Enregistrer"):
        try:
            query = f"""
            INSERT INTO `{PROJECT_ID}.{DATASET_ID}.real_donors`
            (id_donneur, nom_complet, groupe_sanguin, tel, region, adresse, latitude, longitude, numero_proche, notes_sante, date_dernier_don)
            VALUES (
                CAST(FARM_FINGERPRINT(GENERATE_UUID()) AS INT64),
                '{nom}', '{groupe}', '{tel}', '{region}', '{adresse_selectionnee}',
                {latitude}, {longitude},
                '{numero_proche}', '{notes_sante}', CURRENT_DATE()
            )
            """
            client.query(query).result()
            st.success("✅ Donneur ajouté avec succès")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")

# ================================
# CENTRE
# ================================
elif menu == "Centre":
    st.header("Ajouter un centre")

    nom = st.text_input("Nom centre")

    region = st.selectbox("Région", list(REGIONS.keys()))
    adresses = REGIONS[region]

    adresse_selectionnee = st.selectbox("Localisation", [a[0] for a in adresses])

    latitude, longitude = 0, 0
    for a in adresses:
        if a[0] == adresse_selectionnee:
            latitude, longitude = a[1], a[2]

    st.info(f"📍 Latitude: {latitude} | Longitude: {longitude}")

    if st.button("Enregistrer"):
        try:
            query = f"""
            INSERT INTO `{PROJECT_ID}.{DATASET_ID}.real_centers`
            (id_centre, nom, region, latitude, longitude)
            VALUES (
                CAST(FARM_FINGERPRINT(GENERATE_UUID()) AS INT64),
                '{nom}', '{region}', {latitude}, {longitude}
            )
            """
            client.query(query).result()
            st.success("✅ Centre ajouté avec succès")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")

# ================================
# DON
# ================================
elif menu == "Don":
    st.header("Enregistrer un don")

    try:
        # Charger donneurs
        query_donneurs = f"""
        SELECT id_donneur, tel FROM `{PROJECT_ID}.{DATASET_ID}.real_donors`
        """
        donneurs = client.query(query_donneurs).to_dataframe()

        if donneurs.empty:
            st.warning("Aucun donneur disponible")
            st.stop()

        tel_selectionne = st.selectbox("Téléphone donneur", donneurs["tel"])
        id_donneur = int(donneurs[donneurs["tel"] == tel_selectionne]["id_donneur"].values[0])

        # Charger centres
        query_centres = f"""
        SELECT id_centre, nom FROM `{PROJECT_ID}.{DATASET_ID}.real_centers`
        """
        centres = client.query(query_centres).to_dataframe()

        if centres.empty:
            st.warning("Aucun centre disponible")
            st.stop()

        centre_selectionne = st.selectbox("Centre", centres["nom"])
        id_centre = int(centres[centres["nom"] == centre_selectionne]["id_centre"].values[0])

        st.info(f"Donneur ID: {id_donneur}")
        st.info(f"Centre ID: {id_centre}")

        if st.button("Enregistrer"):
            query = f"""
            INSERT INTO `{PROJECT_ID}.{DATASET_ID}.real_donations`
            (id_don, id_donneur, id_centre, date_don)
            VALUES (
                CAST(FARM_FINGERPRINT(GENERATE_UUID()) AS INT64),
                {id_donneur}, {id_centre}, CURRENT_DATE()
            )
            """
            client.query(query).result()
            st.success("✅ Don enregistré avec succès")

    except Exception as e:
        st.error(f"❌ Erreur : {e}")