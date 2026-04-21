import pandas as pd
import os

# =========================
# CHEMINS
# =========================
RAW_PATH = "data/raw/"
PROCESSED_PATH = "data/processed/"

# créer dossier processed si inexistant
os.makedirs(PROCESSED_PATH, exist_ok=True)

# =========================
# CHARGEMENT
# =========================
donors = pd.read_csv(RAW_PATH + "donors.csv")
donations = pd.read_csv(RAW_PATH + "donations.csv")
centers = pd.read_csv(RAW_PATH + "centers.csv")

print("=== CONTRÔLES DE QUALITÉ DES DONNÉES ===")

critical_errors = 0

# =========================
# 1. DONNEURS INCOMPLETS
# =========================
incomplete = donors[
    donors["id_donneur"].isna() |
    donors["groupe_sanguin"].isna() |
    donors["region"].isna() |
    donors["date_dernier_don"].isna()
]

print("\n Vérification : donneurs_incomplets")
if len(incomplete) == 0:
    print(" OK")
else:
    print(f" {len(incomplete)} anomalies détectées")
    critical_errors += 1

# =========================
# 2. GROUPES INVALIDES
# =========================
valid_groups = ['A+','A-','B+','B-','AB+','AB-','O+','O-']

invalid_groups = donors[~donors["groupe_sanguin"].isin(valid_groups)]

print("\n Vérification : groupes_sanguins_invalides")
if len(invalid_groups) == 0:
    print(" OK")
else:
    print(f" {len(invalid_groups)} anomalies détectées")
    critical_errors += 1

# =========================
# 3. COORDONNÉES INVALIDES
# =========================
invalid_coords = donors[
    (donors["latitude"] < 12) | (donors["latitude"] > 17) |
    (donors["longitude"] < -18) | (donors["longitude"] > -11)
]

print("\n Vérification : coordonnees_invalides")
if len(invalid_coords) == 0:
    print(" OK")
else:
    print(f" {len(invalid_coords)} anomalies détectées")
    critical_errors += 1

# =========================
# 4. DOUBLONS
# =========================
duplicates = donors[donors.duplicated(subset=["id_donneur"])]

print("\n Vérification : doublons_donneurs")
if len(duplicates) == 0:
    print(" OK")
else:
    print(f" {len(duplicates)} anomalies détectées")
    critical_errors += 1

# =========================
# 5. DONS ORPHELINS
# =========================
valid_donors_ids = set(donors["id_donneur"])
valid_centers_ids = set(centers["id_centre"])

orphans = donations[
    ~donations["id_donneur"].isin(valid_donors_ids) |
    ~donations["id_centre"].isin(valid_centers_ids)
]

print("\n Vérification : dons_orphelins")
if len(orphans) == 0:
    print(" OK")
else:
    print(f" {len(orphans)} anomalies détectées")
    critical_errors += 1

# =========================
# RÉSULTAT DES CONTRÔLES
# =========================
print("\n=== RÉSUMÉ DES CONTRÔLES ===")
print(f"Nombre de contrôles échoués : {critical_errors}")

if critical_errors > 0:
    raise Exception("❌ PIPELINE ARRÊTÉ : anomalies détectées")

print("✅ Tous les contrôles sont conformes")

# =========================
# TRANSFORMATION (NETTOYAGE)
# =========================

# supprimer lignes invalides
donors_clean = donors[
    donors["id_donneur"].notna() &
    donors["groupe_sanguin"].isin(valid_groups) &
    donors["latitude"].between(12, 17) &
    donors["longitude"].between(-18, -11)
].drop_duplicates(subset=["id_donneur"])

centers_clean = centers.dropna(subset=["id_centre"]).drop_duplicates()

donations_clean = donations[
    donations["id_donneur"].isin(donors_clean["id_donneur"]) &
    donations["id_centre"].isin(centers_clean["id_centre"])
]

# =========================
# SAUVEGARDE
# =========================
donors_clean.to_csv(PROCESSED_PATH + "donors.csv", index=False)
centers_clean.to_csv(PROCESSED_PATH + "centers.csv", index=False)
donations_clean.to_csv(PROCESSED_PATH + "donations.csv", index=False)

print("\n📁 Données néttoyées et sauvegardées dans data/processed/")