import os
import io
import json
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient

# Azurite official development shortcut 
CONN_STR = "UseDevelopmentStorage=true"

CONTAINER = "datasets"
BLOB_NAME  = "All_Diets.csv"

def process_nutritional_data_from_azurite():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*55}")
    print(f"  Serverless Function Triggered — {timestamp}")
    print(f"{'='*55}\n")

    client = BlobServiceClient.from_connection_string(CONN_STR, api_version="2024-08-04")


    # Create container if it doesn't exist
    try:
        client.create_container(CONTAINER)
        print(f"Container '{CONTAINER}' created.")
    except Exception:
        print(f"Container '{CONTAINER}' already exists.")

    # Upload CSV to Azurite Blob Storage
    blob_client = client.get_blob_client(container=CONTAINER, blob=BLOB_NAME)
    with open(BLOB_NAME, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)
    print(f"Uploaded '{BLOB_NAME}' to Azurite container '{CONTAINER}'.\n")

    # Download and process CSV from Azurite
    print("Reading CSV from Azurite Blob Storage...")
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))

    numeric_cols = ['Protein(g)', 'Carbs(g)', 'Fat(g)']
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Calculate insights
    avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean().round(2)
    top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
    highest_protein_diet = avg_macros['Protein(g)'].idxmax()

    print("Average macronutrients per diet type:")
    print(avg_macros.to_string())
    print(f"\nDiet with highest protein: {highest_protein_diet}")

    # Save results to simulated NoSQL
    os.makedirs('simulated_nosql', exist_ok=True)
    result = {
        "processed_at": timestamp,
        "source": f"azurite://{CONTAINER}/{BLOB_NAME}",
        "avg_macros_per_diet": avg_macros.reset_index().to_dict(orient='records'),
        "top_protein_diet": highest_protein_diet,
        "top_5_protein_recipes": top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']].to_dict(orient='records')
    }

    output_path = 'simulated_nosql/results.json'
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\nResults saved to '{output_path}' (simulated NoSQL store).")
    print(f"\n{'='*55}")
    print("  Function completed successfully.")
    print(f"{'='*55}\n")

    return "Data processed and stored successfully."

# Manually invoke the function for testing
if __name__ == "__main__":
    print(process_nutritional_data_from_azurite())