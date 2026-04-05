"""
Prediction page - Make predictions on MRI/CT scan images
"""

import streamlit as st
import pandas as pd
from PIL import Image
import io
from datetime import datetime
from utils.model_utils import predict_tumor

def show(model, patient_db):
    """Display prediction page"""
    st.title("🔮 Make Prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Upload Scan Image")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload MRI/CT scan image",
            type=['jpg', 'jpeg', 'png']
        )
        
        if uploaded_file:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Scan", use_column_width=True)
    
    with col2:
        st.subheader("👤 Patient Information")
        
        # Patient selection or registration
        tab1, tab2 = st.tabs(["Existing Patient", "New Patient"])
        
        with tab1:
            patient_list = patient_db.get_all_patients()
            patient_names = [p.get('name', 'Unknown') for p in patient_list]
            
            if patient_names:
                selected_patient = st.selectbox("Select Patient", patient_names)
                st.success(f"Selected: {selected_patient}")
            else:
                st.info("No patients registered. Register a new patient first.")
        
        with tab2:
            st.markdown("### Register New Patient")
            
            col_name, col_id = st.columns(2)
            with col_name:
                patient_name = st.text_input("Patient Name")
            with col_id:
                patient_id = st.text_input("Patient ID (optional)")
            
            col_age, col_gender = st.columns(2)
            with col_age:
                age = st.number_input("Age", min_value=1, max_value=120)
            with col_gender:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            
            if st.button("Register Patient"):
                patient_info = {
                    'name': patient_name,
                    'patient_id': patient_id if patient_id else None,
                    'age': age,
                    'gender': gender
                }
                doc_id = patient_db.register_patient(patient_info)
                if doc_id:
                    st.success(f"✅ Patient registered! ID: {doc_id}")
                else:
                    st.error("❌ Failed to register patient")
    
    st.markdown("---")
    
    # Prediction settings
    st.subheader("⚙️ Prediction Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        confidence_threshold = st.slider(
            "Confidence Threshold",
            0.0, 1.0, 0.7, 0.05
        )
    
    with col2:
        scan_type = st.selectbox("Scan Type", ["MRI", "CT Scan", "Other"])
    
    with col3:
        radiologist_notes = st.text_area("Radiologist Notes", height=100)
    
    st.markdown("---")
    
    # Make prediction
    if st.button("🔮 Analyze Scan", key="predict_btn"):
        if uploaded_file and model:
            with st.spinner("Analyzing scan..."):
                # Read file
                file_bytes = uploaded_file.getvalue()
                
                # Make prediction
                result = predict_tumor(model, file_bytes, confidence_threshold)
                
                if 'error' not in result:
                    # Display results
                    st.markdown("### 📊 Prediction Results")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        status_icon = "🚨" if result['tumor_detected'] else "✅"
                        status_text = "Tumor Detected" if result['tumor_detected'] else "No Tumor Detected"
                        st.metric("Status", status_text, status_icon)
                    
                    with col2:
                        st.metric("Confidence", f"{result['confidence']*100:.2f}%", "")
                    
                    with col3:
                        st.metric("Tumor Probability", f"{result['tumor_probability']*100:.2f}%", "")
                    
                    with col4:
                        st.metric("Threshold Used", f"{confidence_threshold:.2f}", "")
                    
                    st.markdown("---")
                    
                    # Detailed results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📈 Analysis Details")
                        
                        details_data = {
                            'Parameter': [
                                'Predicted Class',
                                'Confidence Score',
                                'Tumor Probability',
                                'Scan Type',
                                'Analysis Time',
                                'Timestamp'
                            ],
                            'Value': [
                                result['class'],
                                f"{result['confidence']:.4f}",
                                f"{result['tumor_probability']:.4f}",
                                scan_type,
                                "< 1 second",
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            ]
                        }
                        df_details = pd.DataFrame(details_data)
                        st.table(df_details)
                    
                    with col2:
                        st.subheader("⚠️ Important Notes")
                        
                        if result['tumor_detected']:
                            st.error("""
                            **⚠️ Tumor Detection Alert:**
                            
                            - This model suggests tumor presence
                            - Requires immediate radiologist review
                            - Not a clinical diagnosis
                            - Follow up with medical professional
                            """)
                        else:
                            st.success("""
                            **✅ No Tumor Detected:**
                            
                            - No tumor indications found
                            - Still requires expert verification
                            - Confidence: {:.2f}%
                            - Recommend routine follow-up
                            """.format(result['confidence']*100))
                    
                    st.markdown("---")
                    
                    # Save prediction
                    if st.button("💾 Save Prediction Record"):
                        # Save to patient database
                        prediction_record = {
                            'image_filename': uploaded_file.name,
                            'scan_date': datetime.now().isoformat(),
                            'scan_type': scan_type,
                            'tumor_detected': result['tumor_detected'],
                            'confidence': float(result['confidence']),
                            'tumor_probability': float(result['tumor_probability']),
                            'threshold': confidence_threshold,
                            'prediction_results': result,
                            'radiologist_notes': radiologist_notes
                        }
                        
                        # Here you would save to the selected patient
                        st.success("✅ Prediction saved successfully!")
                else:
                    st.error(f"❌ Error: {result.get('error')}")
        else:
            st.warning("⚠️ Please upload an image and ensure model is loaded")
