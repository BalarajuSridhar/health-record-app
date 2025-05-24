import streamlit as st
from utils import save_record, list_patient_records, get_health_trends

st.set_page_config(page_title="Patient Health System")

role = st.sidebar.selectbox("Login As", ["Patient", "Doctor"])
user_id = st.sidebar.text_input("User ID")

if role == "Patient" and user_id:
    st.title(f"Patient Dashboard: {user_id}")
    st.subheader("Upload Health Record")
    uploaded_file = st.file_uploader("Choose file", type=["pdf", "png", "jpg", "txt"])
    record_type = st.selectbox("Record Type", ["Lab Report", "Prescription", "Diagnosis"])
    if st.button("Upload"):
        save_record(user_id, uploaded_file, record_type)
        st.success("Record uploaded successfully!")

    st.subheader("Your Records")
    records = list_patient_records(user_id)
    for rec in records:
        st.json(rec)

elif role == "Doctor" and user_id:
    st.title(f"Doctor Dashboard: {user_id}")
    patient_id = st.text_input("Search Patient ID")
    if patient_id:
        st.subheader(f"Records for Patient {patient_id}")
        records = list_patient_records(patient_id, accessible_by=user_id)
        for rec in records:
            st.json(rec)

        st.subheader("Book Appointment")
        date = st.date_input("Date")
        time = st.time_input("Time")
        if st.button("Book Appointment"):
            st.success(f"Appointment booked with {patient_id} on {date} at {time}")

    st.subheader("Health Trends (Simulated)")
    trends = get_health_trends()
    st.json(trends)