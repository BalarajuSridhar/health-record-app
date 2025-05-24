import os
import json
from datetime import date
from typing import Optional
import streamlit as st

def get_data_path() -> str:
    return "data"

def load_patient_data(pid: str) -> Optional[dict]:
    """Load patient data from a JSON file."""
    path = os.path.join(get_data_path(), f"{pid}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_patient_data(pid: str, data: dict) -> None:
    """Save patient data to a JSON file."""
    os.makedirs(get_data_path(), exist_ok=True)
    path = os.path.join(get_data_path(), f"{pid}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def save_record(pid: str, rtype: str, rdate: date, file) -> None:
    """Add a new record to the patient's data and optionally save the file."""
    data = load_patient_data(pid) or {"ID": pid, "Records": [], "Appointments": []}

    # Optional: Save uploaded file to 'data/uploads/<pid>/'
    uploads_dir = os.path.join(get_data_path(), "uploads", pid)
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    # Add metadata to patient's record
    data["Records"].append({
        "Type": rtype,
        "Date": rdate.strftime("%Y-%m-%d"),
        "File": file.name,
        "FilePath": file_path,
        "Summary": f"{file.name} uploaded",
        "Access Granted To": []
    })

    save_patient_data(pid, data)
