import json
import requests
import time
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

def getNextUrl(bundle: Dict) -> Optional[str]:
    links: List[Dict] = bundle.get("link", [])

    for link in links:
        if link.get("relation") == "next":
            return link.get("url")
        
    return None



def extractResource(resourceType: str, pageSize: int = 20) -> None:
    
    resourceOutputDir = OUTPUT_DIR / resourceType.lower()
    resourceOutputDir.mkdir(parents=True, exist_ok=True)

    url = f"{FHIR_BASE_URL}/{resourceType}"
    params = {"_count": pageSize}

    pageNum = 1

    while url:
    
        response = requests.get(url, params=params if pageNum ==  1 else None, timeout=60)
        response.raise_for_status()
        bundle = response.json()

        outPath = resourceOutputDir / f"{resourceType.lower()}_page_{pageNum}.json"
        saveJson(bundle, outPath)

        url = getNextUrl(bundle)
        pageNum += 1
        params = None
        time.sleep(0.2)

def main() -> None:
    for resource in resources:
        try:
            extractResource(resource)
        except Exception as error:
            print(error)

if __name__ == "__main__":
    main()