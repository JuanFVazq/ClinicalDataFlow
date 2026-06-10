import requests
import json
from pathlib import Path


FHIR_SERVER_URL = "http://localhost:8080/fhir"
SYNTHEA_FHIR_DIR = Path("data/synthea/fhir")



def uploadFiles(filePath: Path):
    with open(filePath, "r", encoding="utf-8") as file:
        bundle = json.load(file)
    
    response = requests.post(
        FHIR_SERVER_URL,
        json=bundle,
        headers={"Content-Type": "application/fhir+json"},
        timeout=60
    )
    if response.status_code in [200, 201]:
        print(f"Uploaded: {filePath.name}")
    else:
        print(f"Failed: {filePath.name}\n"
              f"Status: {response.status_code}")
        print(response.text[:500])
        
def main():
    if not SYNTHEA_FHIR_DIR.exists():
        raise FileNotFoundError(f"Folder not found {SYNTHEA_FHIR_DIR}")

    jsonFiles = list(SYNTHEA_FHIR_DIR.glob("*.json"))
    if not jsonFiles:
        print("No JSON files found.")
        return
    else:
        print(f"Found {len(jsonFiles)} JSON files in {SYNTHEA_FHIR_DIR}")
    
    for filePath in jsonFiles:
        uploadFiles(filePath)


if __name__ == "__main__":
    main()