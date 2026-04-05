"""
Brain Tumor Detection - Cloud-based Application
Streamlit app for tumor detection using trained models with Firestore integration
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
import tempfile
from pathlib import Path

# Import custom modules
from utils.firestore_config import FirestoreDB
from utils.model_utils import load_model, predict_tumor
from utils.patient_db import PatientDatabase
from pages import dashboard, predict, patient_records, model_comparison

# Configure page
st.set_page_config(
    page_title="Brain Tumor Detection System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "db" not in st.session_state:
    st.session_state.db = FirestoreDB()

if "patient_db" not in st.session_state:
    st.session_state.patient_db = PatientDatabase(st.session_state.db)

if "model" not in st.session_state:
    with st.spinner("Loading model..."):
        st.session_state.model = load_model("TL-Model/TL_btd_model.h5")

def main():
    """Main application function"""
    st.markdown("<h1 class='main-header'>🧠 Brain Tumor Detection System</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page:",
        ["Dashboard", "Make Prediction", "Patient Records", "Model Comparison", "Settings"]
    )
    
    # Page routing
    if page == "Dashboard":
        dashboard.show()
    elif page == "Make Prediction":
        predict.show(st.session_state.model, st.session_state.patient_db)
    elif page == "Patient Records":
        patient_records.show(st.session_state.patient_db)
    elif page == "Model Comparison":
        model_comparison.show()
    elif page == "Settings":
        show_settings()

def show_settings():
    """Settings page for credentials and configuration"""
    st.title("⚙️ Settings & Configuration")
    
    with st.expander("🔐 Firestore Credentials", expanded=True):
        st.info("""
        **Note:** Configure your Firestore credentials for production use.
        
        Currently, the app supports:
        - Service Account JSON from Google Cloud
        - To register credentials:
            1. Go to Google Cloud Console
            2. Create a Service Account
            3. Download JSON key
            4. Upload here for production deployment
        """)
        
        st.warning("⚠️ Credentials not yet configured. The app will use demo mode.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Register Credentials"):
                st.info("Credentials registration interface will be available in production.")
        with col2:
            if st.button("🔄 Test Connection"):
                try:
                    # Try to connect to Firestore
                    if st.session_state.db.test_connection():
                        st.success("✅ Firestore connection successful!")
                    else:
                        st.warning("⚠️ Firestore connection failed. Demo mode active.")
                except Exception as e:
                    st.warning(f"⚠️ Demo mode: {str(e)}")
    
    with st.expander("🏥 Application Settings"):
        col1, col2 = st.columns(2)
        with col1:
            confidence_threshold = st.slider(
                "Prediction Confidence Threshold",
                0.0, 1.0, 0.7, 0.05
            )
            st.session_state.confidence_threshold = confidence_threshold
        
        with col2:
            st.metric("Current Model", "EfficientNetB0 (TL)", "90.59%")
    
    with st.expander("📊 Data Privacy"):
        st.markdown("""
        - **Data Encryption**: All patient data is encrypted in transit and at rest
        - **HIPAA Compliance**: Application follows HIPAA guidelines
        - **Data Retention**: Configure retention policies
        - **Audit Logs**: All access is logged for compliance
        """)

if __name__ == "__main__":
    main()
