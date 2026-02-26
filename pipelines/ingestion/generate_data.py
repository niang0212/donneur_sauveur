import pandas as pd
import random
from datetime import datetime, timedelta
import os

# =========================
# CONFIGURATION GLOBALE
# =========================

TOTAL_DONORS = 114_313
OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# REGIONS & COMMUNES (simplifiées)
# =========================

REGIONS = {
    "Dakar": [
        ("Dakar-Plateau", 14.6937, -17.4441),
        ("Pikine", 14.7540, -17.3967),
        ("Guédiawaye", 14.7894, -17.3911),
    ],
    "Thiès": [
        ("Thiès-Ouest", 14.7910, -16.9350),
        ("Mbour", 14.4057, -16.9700),
    ],
    "Saint-Louis": [
        ("Saint-Louis", 16.0179, -16.4896),
    ],
    "Louga": [
        ("Louga", 15.6141, -16.2286),
    ],
    "Diourbel": [
        ("Diourbel", 14.6561, -16.2345),
    ],
    "Fatick": [
        ("Fatick", 14.3390, -16.4115),
    ],
    "Kaolack": [
        ("Kaolack", 14.1516, -16.0726),
    ],
    "Kaffrine": [
        ("Kaffrine", 14.1059, -15.5503),
    ],
    "Tambacounda": [
        ("Tambacounda", 13.7743, -13.6673),
    ],
    "Kédougou": [
        ("Kédougou", 12.5556, -12.1747),
    ],
    "Matam": [
        ("Matam", 15.6556, -13.2553),
    ],
    "Sédhiou": [
        ("Sédhiou", 12.7046, -15.5562),
    ],
    "Ziguinchor": [
        ("Ziguinchor", 12.5833, -16.2667),
    ],
    "Kolda": [
        ("Kolda", 12.8833, -14.9500),
    ],
}

ALL_BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# Régions à déficit
DEFICIT_REGIONS = {
    "Kédougou": ["A+", "B+", "O+"],
    "Matam": ["A+", "O+", "B+"],
    "Sédhiou": ["B+", "O+", "A+"],
}

NOMS = ["Ndiaye", "Diop", "Fall", "Sow", "Ba", "Diallo", "Kane", "Gueye", "Faye",
        "Diakhoumpa","Diagne","gningue","Niang","Diaw","Mendy","Faye","Sonko","Kor","Ndoye",
        "Senghor","Sall","Gaye","Gueye","Cisse","Sy","Niass","Mbacke","Laye","Hanne","Traore","Badji","Badiane",
        "Gomis","Diokh","Diedhiou","Dieng","Pouye","Diene"]
PRENOMS = ["Aminata", "Fatou", "Awa", "Moussa", "Ibrahima", "Cheikh", "Mariama","Aida","Coura","Assane","Malick","Coumba",
           "Yacine","Nogaye","Dior","Samba","Moustapha","Fallou","Alla","Modou","Ousmane","Madicke","Alsanne","Maguette",
           "Pierre","Jean","Jacqueline","louis","Hortence","Khadim","Fallou","Rane","Issa","Mbaye","Dominique","Saliou"]

# =========================
# GENERATION DES DONNEURS
# =========================

donors = []
donors_per_region = TOTAL_DONORS // len(REGIONS)

donor_id = 1

for region, communes in REGIONS.items():
    for _ in range(donors_per_region):
        commune, lat, lon = random.choice(communes)

        blood_groups = (
            DEFICIT_REGIONS.get(region, ALL_BLOOD_GROUPS)
        )

        donors.append({
            "id_donneur": donor_id,
            "nom_complet": f"{random.choice(PRENOMS)} {random.choice(NOMS)}",
            "groupe_sanguin": random.choice(blood_groups),
            "tel": f"7{random.choice([0,6,7,8])}{random.randint(1000000, 9999999)}",
            "region": region,
            "adresse": commune,
            "latitude": lat,
            "longitude": lon,
            "numero_proche": f"7{random.choice([0,6,7,8])}{random.randint(1000000, 9999999)}",
            "notes_sante": random.choice([
                "RAS",
                "Hypertension contrôlée"
            ]),
            "date_dernier_don": (
                datetime.today() - timedelta(days=random.randint(30, 400))
            ).date()
        })

        donor_id += 1

df_donors = pd.DataFrame(donors)

# =========================
# GENERATION DES CENTRES
# =========================

centers = []
center_id = 1

for region, communes in REGIONS.items():
    commune, lat, lon = communes[0]
    centers.append({
        "id_centre": center_id,
        "nom": f"Centre de Transfusion {region}",
        "region": region,
        "latitude": lat,
        "longitude": lon
    })
    center_id += 1

df_centers = pd.DataFrame(centers)

# =========================
# GENERATION DES DONS
# =========================

donations = []
donation_id = 1

for _, donor in df_donors.iterrows():
    if random.random() < 0.6:
        center = df_centers[df_centers["region"] == donor["region"]].iloc[0]
        donations.append({
            "id_don": donation_id,
            "id_donneur": donor["id_donneur"],
            "id_centre": center["id_centre"],
            "date_don": (
                datetime.today() - timedelta(days=random.randint(30, 400))
            ).date()
        })
        donation_id += 1

df_donations = pd.DataFrame(donations)

# =========================
# EXPORT CSV
# =========================

df_donors.to_csv(f"{OUTPUT_DIR}/donors.csv", index=False)
df_centers.to_csv(f"{OUTPUT_DIR}/centers.csv", index=False)
df_donations.to_csv(f"{OUTPUT_DIR}/donations.csv", index=False)

print("Données sénégalaises générées avec succès.")
print(f"Nombre de donneurs : {len(df_donors)}")
print(f"Nombre de centres : {len(df_centers)}")
print(f"Nombre de dons : {len(df_donations)}")
