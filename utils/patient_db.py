"""
Patient database and record management
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid

class PatientDatabase:
    """Patient database management"""
    
    def __init__(self, firestore_db):
        """
        Initialize patient database
        
        Args:
            firestore_db: Firestore DB instance
        """
        self.db = firestore_db
    
    def register_patient(self, patient_info: Dict[str, Any]) -> Optional[str]:
        """
        Register new patient
        
        Args:
            patient_info: Dictionary with patient information
                - name (required)
                - patient_id (optional, auto-generated if not provided)
                - age
                - gender
                - email
                - phone
                - medical_history
                - allergies
                - medications
                - notes
        
        Returns:
            Patient ID if successful, None otherwise
        """
        try:
            # Auto-generate patient ID if not provided
            if 'patient_id' not in patient_info or not patient_info['patient_id']:
                patient_info['patient_id'] = self._generate_patient_id()
            
            # Validate required fields
            if 'name' not in patient_info or not patient_info['name']:
                print("❌ Patient name is required")
                return None
            
            # Set created date
            patient_info['created_at'] = datetime.now().isoformat()
            patient_info['updated_at'] = datetime.now().isoformat()
            patient_info['status'] = 'active'
            
            # Add to database
            doc_id = self.db.add_patient(patient_info)
            print(f"✅ Patient {patient_info['name']} registered successfully")
            return doc_id
        
        except Exception as e:
            print(f"❌ Error registering patient: {str(e)}")
            return None
    
    def get_patient_info(self, patient_id: str) -> Optional[Dict]:
        """Get patient information"""
        try:
            patient = self.db.get_patient(patient_id)
            return patient
        except Exception as e:
            print(f"❌ Error retrieving patient info: {str(e)}")
            return None
    
    def get_all_patients(self) -> List[Dict]:
        """Get all registered patients"""
        try:
            patients = self.db.get_all_patients()
            return patients
        except Exception as e:
            print(f"❌ Error retrieving patients: {str(e)}")
            return []
    
    def update_patient_info(self, patient_id: str, updates: Dict[str, Any]) -> bool:
        """Update patient information"""
        try:
            updates['updated_at'] = datetime.now().isoformat()
            result = self.db.update_patient(patient_id, updates)
            if result:
                print(f"✅ Patient information updated")
            return result
        except Exception as e:
            print(f"❌ Error updating patient: {str(e)}")
            return False
    
    def add_medical_record(self, patient_id: str, record: Dict[str, Any]) -> bool:
        """
        Add medical record for patient
        
        Args:
            patient_id: Patient ID
            record: Medical record data
                - record_type (e.g., 'diagnosis', 'treatment', 'lab_result', 'scan')
                - description
                - date
                - doctor_name
                - notes
        
        Returns:
            True if successful
        """
        try:
            patient = self.get_patient_info(patient_id)
            if not patient:
                print(f"❌ Patient {patient_id} not found")
                return False
            
            if 'medical_records' not in patient:
                patient['medical_records'] = []
            
            record['added_at'] = datetime.now().isoformat()
            record['id'] = str(uuid.uuid4())
            
            patient['medical_records'].append(record)
            self.update_patient_info(patient_id, {'medical_records': patient['medical_records']})
            print(f"✅ Medical record added for patient {patient_id}")
            return True
        
        except Exception as e:
            print(f"❌ Error adding medical record: {str(e)}")
            return False
    
    def add_prediction_record(self, patient_id: str, prediction: Dict[str, Any]) -> bool:
        """
        Add prediction/scan result for patient
        
        Args:
            patient_id: Patient ID
            prediction: Prediction data
                - image_filename
                - scan_date
                - tumor_detected
                - confidence
                - prediction_results
                - radiologist_notes
        
        Returns:
            True if successful
        """
        try:
            patient = self.get_patient_info(patient_id)
            if not patient:
                print(f"❌ Patient {patient_id} not found")
                return False
            
            if 'predictions' not in patient:
                patient['predictions'] = []
            
            prediction['timestamp'] = datetime.now().isoformat()
            prediction['id'] = str(uuid.uuid4())
            
            patient['predictions'].append(prediction)
            self.update_patient_info(patient_id, {'predictions': patient['predictions']})
            
            # Also add to Firestore predictions collection
            self.db.add_prediction(patient_id, prediction)
            print(f"✅ Prediction record added for patient {patient_id}")
            return True
        
        except Exception as e:
            print(f"❌ Error adding prediction record: {str(e)}")
            return False
    
    def get_patient_predictions(self, patient_id: str) -> List[Dict]:
        """Get all predictions for a patient"""
        try:
            patient = self.get_patient_info(patient_id)
            if patient and 'predictions' in patient:
                return patient['predictions']
            return []
        except Exception as e:
            print(f"❌ Error retrieving predictions: {str(e)}")
            return []
    
    def get_patient_medical_history(self, patient_id: str) -> Dict:
        """Get patient's medical history summary"""
        try:
            patient = self.get_patient_info(patient_id)
            if not patient:
                return {}
            
            history = {
                'patient_id': patient_id,
                'name': patient.get('name'),
                'age': patient.get('age'),
                'gender': patient.get('gender'),
                'medical_records': patient.get('medical_records', []),
                'predictions': patient.get('predictions', []),
                'allergies': patient.get('allergies', []),
                'medications': patient.get('medications', []),
                'notes': patient.get('notes', ''),
                'created_at': patient.get('created_at'),
                'last_updated': patient.get('updated_at')
            }
            return history
        
        except Exception as e:
            print(f"❌ Error retrieving medical history: {str(e)}")
            return {}
    
    def search_patients(self, query: str) -> List[Dict]:
        """
        Search patients by name or ID
        
        Args:
            query: Search term
        
        Returns:
            List of matching patients
        """
        try:
            all_patients = self.get_all_patients()
            query_lower = query.lower()
            
            results = []
            for patient in all_patients:
                if (query_lower in patient.get('name', '').lower() or
                    query_lower in patient.get('patient_id', '').lower()):
                    results.append(patient)
            
            return results
        except Exception as e:
            print(f"❌ Error searching patients: {str(e)}")
            return []
    
    @staticmethod
    def _generate_patient_id() -> str:
        """Generate unique patient ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = str(uuid.uuid4())[:8].upper()
        return f"BTD-{timestamp}-{random_suffix}"
