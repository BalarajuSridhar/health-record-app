
import streamlit as st
from utils import save_record, load_patient_data, save_patient_data
from datetime import datetime

st.set_page_config(page_title="Health Records App", page_icon="🩺")
st.title("🩺 Patient Health Records & Appointment System")

# Sidebar for role selection
role = st.sidebar.radio("Login as", ["Patient", "Doctor"], index=0)

# -------------------- PATIENT VIEW --------------------
if role == "Patient":
    st.header("📤 Upload Your Health Record")

    patient_id = st.text_input("Your Patient ID", placeholder="e.g. P123")
    record_type = st.selectbox("Select Record Type", ["Lab Report", "Prescription", "Scan", "Other"])
    record_date = st.date_input("Record Date")
    uploaded_file = st.file_uploader("Choose a file (PDF/Image/Text)", type=["pdf", "jpg", "png", "txt"])

    if st.button("Upload Record"):
        if patient_id and uploaded_file:
            save_record(patient_id, record_type, record_date, uploaded_file)
            st.success("✅ Record uploaded successfully!")
        else:
            st.warning("⚠️ Please provide both Patient ID and a file to upload.")

    st.divider()
    st.header("📁 View My Records & Appointments")
    
    if patient_id:
        data = load_patient_data(patient_id)
        if data:
            st.subheader(f"📄 Records for Patient ID: {patient_id}")
            st.json(data)
        else:
            st.info("No records found for this ID.")
    else:
        st.info("Enter Patient ID to view your records.")

# -------------------- DOCTOR VIEW --------------------
elif role == "Doctor":
    st.header("🔍 View Patient Records")
    
    search_id = st.text_input("Enter Patient ID to View Records")
    if st.button("View Patient"):
        if search_id:
            patient_data = load_patient_data(search_id)
            if patient_data:
                st.success(f"📂 Found records for {search_id}")
                st.json(patient_data)
            else:
                st.error("❌ No data found for that ID.")
        else:
            st.warning("⚠️ Please enter a Patient ID.")

    st.divider()
    st.header("📅 Book Appointment")

    pid = st.text_input("Patient ID for Appointment")
    doc_name = st.text_input("Your Name (Doctor)")
    appt_date = st.date_input("Appointment Date")

    if st.button("Confirm Appointment"):
        if pid and doc_name:
            patient_data = load_patient_data(pid) or {"ID": pid, "Records": [], "Appointments": []}
            appointment = {
                "Doctor": doc_name,
                "Date": appt_date.strftime("%Y-%m-%d"),
                "Status": "Confirmed"
            }
            if "Appointments" not in patient_data:
                patient_data["Appointments"] = []
            patient_data["Appointments"].append(appointment)
            save_patient_data(pid, patient_data)
            st.success(f"✅ Appointment booked with {pid} on {appt_date.strftime('%Y-%m-%d')}")
        else:
            st.warning("⚠️ Please provide both Patient ID and your name.")
