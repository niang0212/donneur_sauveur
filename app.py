import streamlit as st
from google.cloud import bigquery

PROJECT_ID = "donneursauveur-486312"
DATASET_ID = "donneur_sauveur"

from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    "secrets/sa-donneur-sauveur.json"
)

client = bigquery.Client(
    credentials=credentials,
    project=PROJECT_ID
)

st.title("Gestion des Donneurs")

menu = st.sidebar.selectbox("Menu", ["Donneur", "Centre", "Don"])

# ======================
# DONNEUR
# ======================
if menu == "Donneur":
    st.header("Ajouter un donneur")

    nom = st.text_input("Nom complet")
    groupe = st.selectbox("Groupe sanguin", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
    tel = st.text_input("Téléphone")
    region = st.text_input("Région")
    adresse = st.text_input("Adresse")
    latitude = st.number_input("Latitude")
    longitude = st.number_input("Longitude")

    if st.button("Enregistrer"):
        query = f"""
        INSERT INTO `{PROJECT_ID}.{DATASET_ID}.raw_donors`
        (id_donneur, nom_complet, groupe_sanguin, tel, region, adresse, latitude, longitude, date_dernier_don)
        VALUES (
            CAST(FARM_FINGERPRINT(GENERATE_UUID()) AS INT64),
            '{nom}', '{groupe}', '{tel}', '{region}', '{adresse}', {latitude}, {longitude}, CURRENT_DATE()
        )
        """
        client.query(query)
        st.success("Donneur ajouté avec succès")

# ======================
# CENTRE
# ======================
elif menu == "Centre":
    st.header("Ajouter un centre")

    nom = st.text_input("Nom centre")
    region = st.text_input("Région")
    latitude = st.number_input("Latitude")
    longitude = st.number_input("Longitude")

    if st.button("Enregistrer"):
        query = f"""
        INSERT INTO `{PROJECT_ID}.{DATASET_ID}.raw_centers`
        (id_centre, nom, region, latitude, longitude)
        VALUES (
            CAST(FARM_FINGERPRINT(GENERATE_UUID()) AS INT64),
            '{nom}', '{region}', {latitude}, {longitude}
        )
        """
        client.query(query)
        st.success("Centre ajouté avec succès")

# ======================
# DON
# ======================
elif menu == "Don":
    st.header("Enregistrer un don")

    id_donneur = st.number_input("ID donneur")
    id_centre = st.number_input("ID centre")

    if st.button("Enregistrer"):
        query = f"""
        INSERT INTO `{PROJECT_ID}.{DATASET_ID}.raw_donations`
        (id_don, id_donneur, id_centre, date_don)
        VALUES (
            CAST(FARM_FINGERPRINT(GENERATE_UUID()) AS INT64),
            {id_donneur}, {id_centre}, CURRENT_DATE()
        )
        """
        client.query(query)
        st.success("Don enregistré avec succès")