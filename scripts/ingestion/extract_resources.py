import json
import requests
from pathlib import Path
from typing import Dict, List, Optional

FHIR_BASE_URL = "http://localhost:8080/fhir"
OUTPUT_DIR = Path("data/raw/fhir_api")

resources = [
    "Patient",
    "Encounter",
    "Condition",
    "Observation",
    "MedicationRequest",
    "Procedure",
    "AllergyIntolerance",
    "Immunization",
]


def saveJson(data: Dict, outputPath: Path) -> None:
    outputPath.parent.mkdir(parents=True, exist_ok=True)

    with open(outputPath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

def extractResource(resourceType: str) -> None:
    
    resourceOutputDir = OUTPUT_DIR / resourceType.lower()
    resourceOutputDir.mkdir(parents=True, exist_ok=True)

    url = f"{FHIR_BASE_URL}/{resourceType}"
    
    response = requests.get(url)
    response.raise_for_status()
    bundle = response.json()

    outPath = resourceOutputDir / f"{resourceType.lower()}.json"
    saveJson(bundle, outPath)

def main() -> None:
    for resource in resources:
        try:
            extractResource(resource)
        except Exception as error:
            print(error)

if __name__ == "__main__":
    main()