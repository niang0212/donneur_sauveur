import pandas as pd
import random
from datetime import datetime, timedelta
import os

# =========================
# CONFIGURATION GLOBALE
# =========================

TOTAL_DONORS = 13_313
OUTPUT_DIR = "data/raw"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# REGIONS & COMMUNES (simplifiées)
# =========================

REGIONS = {
    "Dakar": [
        ("Dakar", 14.7167, -17.4677),
        ("Guédiawaye", 14.7833, -17.3833),
        ("Pikine", 14.7500, -17.4000),
        ("Rufisque", 14.7167, -17.2667),
        ("Keur Massar", 14.7800, -17.3000),
    ],
    "Thiès": [
        ("Thiès", 14.7900, -16.9200),
        ("Mbour", 14.4100, -16.9600),
        ("Tivaouane", 14.9500, -16.8200),
    ],
    "Saint-Louis": [
        ("Saint-Louis", 16.0200, -16.5000),
        ("Dagana", 16.5100, -15.5100),
        ("Podor", 16.6200, -14.9600),
    ],
    "Louga": [
        ("Louga", 15.6100, -16.2200),
        ("Linguère", 15.3900, -15.1200),
        ("Kébémer", 15.3700, -16.4500),
    ],
    "Diourbel": [
        ("Diourbel", 14.6500, -16.2300),
        ("Bambey", 14.7000, -16.4500),
        ("Mbacké", 14.7900, -15.9100),
    ],
    "Fatick": [
        ("Fatick", 14.3300, -16.4000),
        ("Foundiougne", 14.1300, -16.4700),
        ("Gossas", 14.4900, -16.0700),
    ],
    "Kaolack": [
        ("Kaolack", 14.1600, -16.0800),
        ("Guinguinéo", 14.2700, -15.9500),
        ("Nioro du Rip", 13.7500, -15.7800),
    ],
    "Kaffrine": [
        ("Kaffrine", 14.1000, -15.5500),
        ("Birkelane", 14.1300, -15.7500),
        ("Koungheul", 13.9800, -14.8000),
        ("Malem Hodar", 14.1600, -15.3100),
    ],
    "Tambacounda": [
        ("Tambacounda", 13.7700, -13.6700),
        ("Bakel", 14.9000, -12.4500),
        ("Goudiry", 14.2800, -13.2700),
        ("Koupentoum", 13.9900, -14.5600),
    ],
    "Kédougou": [
        ("Kédougou", 12.5500, -12.1800),
        ("Salémata", 12.6300, -12.8200),
        ("Saraya", 12.8300, -11.7500),
    ],
    "Kolda": [
        ("Kolda", 12.8800, -14.9400),
        ("Médina Yoro Foulah", 13.0400, -14.7100),
        ("Vélingara", 13.1500, -14.1100),
    ],
    "Sédhiou": [
        ("Sédhiou", 12.7000, -15.5500),
        ("Bounkiling", 13.0200, -15.5300),
        ("Goudomp", 12.5700, -15.7500),
    ],
    "Ziguinchor": [
        ("Ziguinchor", 12.5800, -16.2700),
        ("Bignona", 12.8100, -16.2300),
        ("Oussouye", 12.4800, -16.5400),
    ],
    "Matam": [
        ("Matam", 15.6500, -13.2500),
        ("Kanel", 15.4900, -13.1700),
        ("Ranérou Ferlo", 15.3000, -13.9700),
    ],
}

ALL_BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# Régions à déficit
DEFICIT_REGIONS = {
    "Kédougou": ["A+", "B+", "O+"],
    "Matam": ["AB+", "AB-", "O+"],
    "Sédhiou": ["B-", "O-", "A+"],
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
        "nom": f"{region}_Centre de Transfusion ",
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
