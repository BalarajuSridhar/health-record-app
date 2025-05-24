import os
import json
from datetime import datetime

DATA_DIR = "records/"
os.makedirs(DATA_DIR, exist_ok=True)

def save_record(patient_id, file, record_type):
    if file:
        content = file.read()
        filename = f"{patient_id}_{datetime.now().isoformat()}_{file.name}"
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(content)
        metadata = {
            "patient_id": patient_id,
            "filename": filename,
            "record_type": record_type,
            "uploaded": str(datetime.now()),
            "access_granted": []
        }
        with open(filepath + ".meta.json", "w") as f:
            json.dump(metadata, f)

def list_patient_records(patient_id, accessible_by=None):
    results = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".meta.json"):
            with open(os.path.join(DATA_DIR, file)) as f:
                meta = json.load(f)
                if meta["patient_id"] == patient_id:
                    if accessible_by and accessible_by not in meta["access_granted"]:
                        continue
                    results.append(meta)
    return results

def get_health_trends():
    return {
        "Blood Pressure": "120/80 mmHg (Avg)",
        "Glucose": "98 mg/dL",
    }