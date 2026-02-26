CREATE OR REPLACE TABLE donneur_sauveur.raw_donors (
  id_donneur INT64,
  nom_complet STRING,
  groupe_sanguin STRING,
  tel STRING,
  region STRING,
  adresse STRING,
  latitude FLOAT64,
  longitude FLOAT64,
  numero_proche STRING,
  notes_sante STRING,
  date_dernier_don DATE
);

CREATE OR REPLACE TABLE donneur_sauveur.raw_centers (
  id_centre INT64,
  nom STRING,
  region STRING,
  latitude FLOAT64,
  longitude FLOAT64
);

CREATE OR REPLACE TABLE donneur_sauveur.raw_donations (
  id_don INT64,
  id_donneur INT64,
  id_centre INT64,
  date_don DATE
);
