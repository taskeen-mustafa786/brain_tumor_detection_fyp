"""
Firestore configuration and database management
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class FirestoreDB:
    """Firebase Firestore database wrapper"""
    
    def __init__(self, credentials_path: str = None):
        """
        Initialize Firestore database connection
        
        Args:
            credentials_path: Path to Google Cloud service account JSON
        """
        self.credentials_path = credentials_path
        self.db = None
        self.connected = False
        self._initialize_connection()
    
    def _initialize_connection(self):
        """Initialize Firestore connection"""
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            if self.credentials_path and os.path.exists(self.credentials_path):
                # Initialize with credentials
                cred = credentials.Certificate(self.credentials_path)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.connected = True
                print("✅ Firestore connected successfully")
            else:
                # Initialize without credentials (demo mode)
                print("⚠️ Demo mode: Firestore credentials not configured")
                self.connected = False
        except Exception as e:
            print(f"⚠️ Firestore initialization error: {str(e)}")
            print("Running in demo mode")
            self.connected = False
    
    def test_connection(self) -> bool:
        """Test Firestore connection"""
        if self.db is None:
            return False
        try:
            # Try to read from a collection
            self.db.collection('_test').limit(1).stream()
            return True
        except Exception:
            return False
    
    def add_patient(self, patient_data: Dict[str, Any]) -> str:
        """
        Add new patient record to Firestore
        
        Args:
            patient_data: Dictionary containing patient information
        
        Returns:
            Patient document ID
        """
        if not self.connected:
            return self._demo_add_patient(patient_data)
        
        try:
            patient_data['created_at'] = datetime.now()
            patient_data['updated_at'] = datetime.now()
            
            doc_ref = self.db.collection('patients').add(patient_data)
            return doc_ref[1].id
        except Exception as e:
            print(f"Error adding patient: {str(e)}")
            return None
    
    def get_patient(self, patient_id: str) -> Optional[Dict]:
        """Get patient record by ID"""
        if not self.connected:
            return self._demo_get_patient(patient_id)
        
        try:
            doc = self.db.collection('patients').document(patient_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Error retrieving patient: {str(e)}")
            return None
    
    def get_all_patients(self) -> List[Dict]:
        """Get all patient records"""
        if not self.connected:
            return self._demo_get_all_patients()
        
        try:
            docs = self.db.collection('patients').stream()
            patients = []
            for doc in docs:
                patient_data = doc.to_dict()
                patient_data['id'] = doc.id
                patients.append(patient_data)
            return patients
        except Exception as e:
            print(f"Error retrieving patients: {str(e)}")
            return []
    
    def update_patient(self, patient_id: str, updates: Dict[str, Any]) -> bool:
        """Update patient record"""
        if not self.connected:
            return self._demo_update_patient(patient_id, updates)
        
        try:
            updates['updated_at'] = datetime.now()
            self.db.collection('patients').document(patient_id).update(updates)
            return True
        except Exception as e:
            print(f"Error updating patient: {str(e)}")
            return False
    
    def add_prediction(self, patient_id: str, prediction_data: Dict[str, Any]) -> str:
        """Add prediction record for patient"""
        if not self.connected:
            return self._demo_add_prediction(patient_id, prediction_data)
        
        try:
            prediction_data['timestamp'] = datetime.now()
            prediction_data['patient_id'] = patient_id
            
            doc_ref = self.db.collection('predictions').add(prediction_data)
            return doc_ref[1].id
        except Exception as e:
            print(f"Error adding prediction: {str(e)}")
            return None
    
    def get_patient_predictions(self, patient_id: str) -> List[Dict]:
        """Get all predictions for a patient"""
        if not self.connected:
            return self._demo_get_patient_predictions(patient_id)
        
        try:
            docs = self.db.collection('predictions')\
                .where('patient_id', '==', patient_id)\
                .order_by('timestamp', direction='DESCENDING')\
                .stream()
            
            predictions = []
            for doc in docs:
                pred_data = doc.to_dict()
                pred_data['id'] = doc.id
                predictions.append(pred_data)
            return predictions
        except Exception as e:
            print(f"Error retrieving predictions: {str(e)}")
            return []
    
    # Demo mode methods for testing without Firestore credentials
    def _demo_add_patient(self, patient_data: Dict) -> str:
        """Demo: Add patient to in-memory storage"""
        if not hasattr(self, '_demo_patients'):
            self._demo_patients = {}
            self._demo_next_id = 1
        
        patient_id = f"demo_patient_{self._demo_next_id}"
        patient_data['created_at'] = datetime.now()
        patient_data['updated_at'] = datetime.now()
        self._demo_patients[patient_id] = patient_data
        self._demo_next_id += 1
        return patient_id
    
    def _demo_get_patient(self, patient_id: str) -> Optional[Dict]:
        """Demo: Get patient from in-memory storage"""
        if hasattr(self, '_demo_patients'):
            return self._demo_patients.get(patient_id)
        return None
    
    def _demo_get_all_patients(self) -> List[Dict]:
        """Demo: Get all patients from in-memory storage"""
        if hasattr(self, '_demo_patients'):
            patients = []
            for pid, data in self._demo_patients.items():
                patient_copy = data.copy()
                patient_copy['id'] = pid
                patients.append(patient_copy)
            return patients
        return []
    
    def _demo_update_patient(self, patient_id: str, updates: Dict) -> bool:
        """Demo: Update patient in in-memory storage"""
        if hasattr(self, '_demo_patients') and patient_id in self._demo_patients:
            updates['updated_at'] = datetime.now()
            self._demo_patients[patient_id].update(updates)
            return True
        return False
    
    def _demo_add_prediction(self, patient_id: str, prediction_data: Dict) -> str:
        """Demo: Add prediction to in-memory storage"""
        if not hasattr(self, '_demo_predictions'):
            self._demo_predictions = []
        
        prediction_data['timestamp'] = datetime.now()
        prediction_data['patient_id'] = patient_id
        prediction_data['id'] = f"demo_pred_{len(self._demo_predictions)}"
        self._demo_predictions.append(prediction_data)
        return prediction_data['id']
    
    def _demo_get_patient_predictions(self, patient_id: str) -> List[Dict]:
        """Demo: Get predictions from in-memory storage"""
        if hasattr(self, '_demo_predictions'):
            return [p for p in self._demo_predictions if p.get('patient_id') == patient_id]
        return []
