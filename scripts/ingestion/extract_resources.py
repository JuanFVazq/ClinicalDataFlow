import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional

FHIR_BASE_URL = "https://localhost:8080/fhir"
OUTPUT_DIR = Path("data/raw/fhir_api")

resources = [
    "Patient",
    "Encounter",
    "Condition",
    "Observation",
    "MedicationRequest",
    "AllergyIntolerance",
    "Immunization"
]

def saveJson(data: Dict, outputPath: Path) -> None:
    outputPath.parent.mkdir(parents=True, exist_ok=True)

    with open(outputPath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)