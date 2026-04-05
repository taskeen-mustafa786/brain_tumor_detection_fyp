"""
Patient Records page - Manage patient data and medical history
"""

import streamlit as st
import pandas as pd
from datetime import datetime

def show(patient_db):
    """Display patient records page"""
    st.title("👥 Patient Records & Medical History")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Search Patients",
        "Patient Details",
        "Medical History",
        "Add Record"
    ])
    
    with tab1:
        st.subheader("🔍 Search Patients")
        
        search_query = st.text_input("Search by name or patient ID")
        
        if search_query:
            results = patient_db.search_patients(search_query)
            
            if results:
                st.success(f"Found {len(results)} patient(s)")
                
                for patient in results:
                    with st.expander(f"👤 {patient.get('name', 'Unknown')} - {patient.get('patient_id', 'N/A')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Patient ID:** {patient.get('patient_id', 'N/A')}")
                            st.write(f"**Age:** {patient.get('age', 'N/A')}")
                            st.write(f"**Gender:** {patient.get('gender', 'N/A')}")
                            st.write(f"**Email:** {patient.get('email', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Phone:** {patient.get('phone', 'N/A')}")
                            st.write(f"**Status:** {patient.get('status', 'Active')}")
                            st.write(f"**Created:** {patient.get('created_at', 'N/A')}")
                            st.write(f"**Updated:** {patient.get('updated_at', 'N/A')}")
            else:
                st.info("No patients found matching your search")
        else:
            # Show all patients
            all_patients = patient_db.get_all_patients()
            if all_patients:
                patient_names = [f"{p.get('name', 'Unknown')} ({p.get('patient_id', 'N/A')})" for p in all_patients]
                st.info(f"{len(all_patients)} patient(s) registered in system")
                
                for idx, patient in enumerate(all_patients):
                    with st.expander(f"👤 {patient.get('name', 'Unknown')} - {patient.get('patient_id', 'N/A')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Patient ID:** {patient.get('patient_id', 'N/A')}")
                            st.write(f"**Age:** {patient.get('age', 'N/A')}")
                            st.write(f"**Gender:** {patient.get('gender', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Status:** {patient.get('status', 'Active')}")
                            st.write(f"**Registered:** {patient.get('created_at', 'N/A')}")
            else:
                st.info("No patients registered yet")
    
    with tab2:
        st.subheader("📋 Patient Details")
        
        patients = patient_db.get_all_patients()
        if patients:
            patient_options = {p.get('name', 'Unknown'): p for p in patients}
            selected_patient_name = st.selectbox("Select Patient", list(patient_options.keys()))
            selected_patient = patient_options[selected_patient_name]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👤 Personal Information")
                
                personal_data = {
                    'Field': [
                        'Name',
                        'Patient ID',
                        'Age',
                        'Gender',
                        'Email',
                        'Phone'
                    ],
                    'Value': [
                        selected_patient.get('name', 'N/A'),
                        selected_patient.get('patient_id', 'N/A'),
                        selected_patient.get('age', 'N/A'),
                        selected_patient.get('gender', 'N/A'),
                        selected_patient.get('email', 'N/A'),
                        selected_patient.get('phone', 'N/A')
                    ]
                }
                df_personal = pd.DataFrame(personal_data)
                st.table(df_personal)
            
            with col2:
                st.subheader("📋 Medical Information")
                
                medical_data = {
                    'Category': [
                        'Allergies',
                        'Current Medications',
                        'Medical History',
                        'Status',
                        'Created',
                        'Last Updated'
                    ],
                    'Value': [
                        ', '.join(selected_patient.get('allergies', [])) or 'None',
                        ', '.join(selected_patient.get('medications', [])) or 'None',
                        selected_patient.get('medical_notes', 'N/A'),
                        selected_patient.get('status', 'Active'),
                        selected_patient.get('created_at', 'N/A'),
                        selected_patient.get('updated_at', 'N/A')
                    ]
                }
                df_medical = pd.DataFrame(medical_data)
                st.table(df_medical)
            
            st.markdown("---")
            
            # Edit patient info
            st.subheader("✏️ Edit Patient Information")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_age = st.number_input("Update Age", value=selected_patient.get('age', 0))
            with col2:
                new_email = st.text_input("Update Email", value=selected_patient.get('email', ''))
            with col3:
                new_phone = st.text_input("Update Phone", value=selected_patient.get('phone', ''))
            
            if st.button("💾 Update Patient Info"):
                updates = {
                    'age': new_age,
                    'email': new_email,
                    'phone': new_phone
                }
                patient_db.update_patient_info(selected_patient['id'], updates)
                st.success("✅ Patient information updated!")
        else:
            st.info("No patients registered yet")
    
    with tab3:
        st.subheader("📖 Medical History & Records")
        
        patients = patient_db.get_all_patients()
        if patients:
            patient_options = {p.get('name', 'Unknown'): p for p in patients}
            selected_patient_name = st.selectbox("Select Patient", list(patient_options.keys()), key="history_select")
            selected_patient = patient_options[selected_patient_name]
            
            # Medical Records
            medical_records = selected_patient.get('medical_records', [])
            
            if medical_records:
                st.subheader(f"📋 Medical Records for {selected_patient.get('name')}")
                
                for record in medical_records:
                    with st.expander(f"📄 {record.get('record_type', 'Record')} - {record.get('date', 'N/A')}"):
                        cols = st.columns(2)
                        with cols[0]:
                            st.write(f"**Type:** {record.get('record_type', 'N/A')}")
                            st.write(f"**Date:** {record.get('date', 'N/A')}")
                            st.write(f"**Doctor:** {record.get('doctor_name', 'N/A')}")
                        with cols[1]:
                            st.write(f"**Description:**\n{record.get('description', 'N/A')}")
                            st.write(f"**Notes:**\n{record.get('notes', 'None')}")
            else:
                st.info("No medical records available for this patient")
            
            # Prediction History
            st.markdown("---")
            predictions = selected_patient.get('predictions', [])
            
            if predictions:
                st.subheader(f"🔮 Prediction History for {selected_patient.get('name')}")
                
                for pred in predictions:
                    with st.expander(f"🔍 Scan - {pred.get('timestamp', 'N/A')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            status = "🚨 Tumor Detected" if pred.get('tumor_detected') else "✅ No Tumor"
                            st.write(f"**Status:** {status}")
                            st.write(f"**Confidence:** {pred.get('confidence', 0)*100:.2f}%")
                            st.write(f"**Scan Type:** {pred.get('scan_type', 'N/A')}")
                        
                        with col2:
                            st.write(f"**File:** {pred.get('image_filename', 'N/A')}")
                            st.write(f"**Timestamp:** {pred.get('timestamp', 'N/A')}")
                            st.write(f"**Radiologist Notes:** {pred.get('radiologist_notes', 'None')}")
            else:
                st.info("No predictions available for this patient")
        else:
            st.info("No patients registered yet")
    
    with tab4:
        st.subheader("➕ Add Medical Record")
        
        patients = patient_db.get_all_patients()
        if patients:
            patient_options = {p.get('name', 'Unknown'): p for p in patients}
            selected_patient_name = st.selectbox("Select Patient", list(patient_options.keys()), key="add_record_select")
            selected_patient = patient_options[selected_patient_name]
            
            col1, col2 = st.columns(2)
            
            with col1:
                record_type = st.selectbox(
                    "Record Type",
                    ["diagnosis", "treatment", "lab_result", "scan", "appointment", "other"]
                )
                record_date = st.date_input("Record Date")
                doctor_name = st.text_input("Doctor/Provider Name")
            
            with col2:
                description = st.text_area("Record Description")
                notes = st.text_area("Additional Notes")
            
            if st.button("➕ Add Record"):
                record = {
                    'record_type': record_type,
                    'date': str(record_date),
                    'doctor_name': doctor_name,
                    'description': description,
                    'notes': notes
                }
                
                if patient_db.add_medical_record(selected_patient['id'], record):
                    st.success(f"✅ Record added for {selected_patient.get('name')}")
                else:
                    st.error("❌ Failed to add record")
        else:
            st.info("No patients registered yet. Register a patient first.")
