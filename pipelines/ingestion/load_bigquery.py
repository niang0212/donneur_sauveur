from google.cloud import bigquery
import os

PROJECT_ID = "donneursauveur-486312"
DATASET_ID = "donneur_sauveur"
DATA_DIR = "data/processed"

client = bigquery.Client(project=PROJECT_ID)

def load_csv(table_name, file_name):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE"
    )

    with open(os.path.join(DATA_DIR, file_name), "rb") as f:
        job = client.load_table_from_file(
            f,
            table_id,
            job_config=job_config
        )

    job.result()
    print(f"Table {table_name} chargée avec succès.")

if __name__ == "__main__":
    load_csv("processed_donors", "donors.csv")
    load_csv("processed_centers", "centers.csv")
    load_csv("processed_donations", "donations.csv")
