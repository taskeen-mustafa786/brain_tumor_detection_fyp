"""
Firestore database configuration and operations
"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# Try to import Firebase, but make it optional
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("⚠️ Firebase not installed - using demo mode")

# Try to import Streamlit for secrets
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

from dotenv import load_dotenv
load_dotenv()

class FirestoreDB:
    """Firestore database operations"""

    def __init__(self):
        self.db = None
        self.demo_mode = not FIREBASE_AVAILABLE

        if not self.demo_mode:
            try:
                # Check if Firebase app is already initialized
                if not firebase_admin._apps:
                    # Try to get credentials from Streamlit secrets first
                    cred_dict = None
                    if STREAMLIT_AVAILABLE and hasattr(st, 'secrets'):
                        try:
                            secrets = st.secrets
                            cred_dict = {
                                "type": "service_account",
                                "project_id": secrets.get("FIREBASE_PROJECT_ID"),
                                "private_key_id": secrets.get("FIREBASE_PRIVATE_KEY_ID"),
                                "private_key": secrets.get("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                                "client_email": secrets.get("FIREBASE_CLIENT_EMAIL"),
                                "client_id": secrets.get("FIREBASE_CLIENT_ID"),
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token",
                                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                                "client_x509_cert_url": secrets.get("FIREBASE_CLIENT_X509_CERT_URL")
                            }
                        except Exception as e:
                            print(f"⚠️ Could not load Streamlit secrets: {e}")

                    # If Streamlit secrets not available, try environment variables
                    if not cred_dict or not all(cred_dict.values()):
                        cred_dict = {
                            "type": "service_account",
                            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                            "private_key": os.getenv("FIREBASE_PRIVATE_KEY", "").replace("\\n", "\n"),
                            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
                        }

                    # If credentials are not set, try using the key file path
                    key_file = os.getenv("FIREBASE_KEY_FILE")
                    if key_file and os.path.exists(key_file):
                        cred = credentials.Certificate(key_file)
                    elif all(cred_dict.values() if cred_dict else []):
                        cred = credentials.Certificate(cred_dict)
                    else:
                        print("⚠️ Firebase credentials not found - using demo mode")
                        self.demo_mode = True
                        return

                    firebase_admin.initialize_app(cred)

                self.db = firestore.client()
                print("✅ Firestore connected successfully")

            except Exception as e:
                print(f"❌ Firestore connection failed: {str(e)}")
                self.demo_mode = True
        else:
            print("⚠️ Firebase not available - using demo mode")

    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """Create a new user"""
        if self.demo_mode:
            print(f"📝 Demo: Created user {user_data['email']}")
            return True

        try:
            user_ref = self.db.collection('users').document(user_data['email'])
            user_ref.set(user_data)
            return True
        except Exception as e:
            print(f"❌ Error creating user: {str(e)}")
            return False

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        if self.demo_mode:
            return {
                "email": email,
                "name": email.split('@')[0],
                "role": "patient",
                "patient_id": f"P{hash(email) % 10000:04d}",
                "created_at": datetime.utcnow().isoformat()
            }

        try:
            user_ref = self.db.collection('users').document(email)
            user_doc = user_ref.get()
            if user_doc.exists:
                return user_doc.to_dict()
            return None
        except Exception as e:
            print(f"❌ Error getting user: {str(e)}")
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user (simplified - in production use Firebase Auth)"""
        if self.demo_mode:
            # Demo authentication - accept any password with 8+ chars
            if len(password) >= 8:
                return self.get_user(email)
            return None

        try:
            # In production, use Firebase Auth for proper authentication
            # For now, just check if user exists
            user = self.get_user(email)
            if user:
                # TODO: Implement proper password verification with Firebase Auth
                return user
            return None
        except Exception as e:
            print(f"❌ Error authenticating user: {str(e)}")
            return None

    def save_prediction(self, prediction_data: Dict[str, Any]) -> bool:
        """Save prediction result"""
        if self.demo_mode:
            print(f"📝 Demo: Saved prediction for {prediction_data.get('user_email', 'unknown')}")
            return True

        try:
            # Add timestamp if not present
            if 'timestamp' not in prediction_data:
                prediction_data['timestamp'] = datetime.utcnow().isoformat()

            # Save to predictions collection
            prediction_ref = self.db.collection('predictions').document()
            prediction_ref.set(prediction_data)

            # Update patient's prediction history
            patient_id = prediction_data.get('patient_id')
            if patient_id:
                self._update_patient_predictions(patient_id, prediction_data)

            return True
        except Exception as e:
            print(f"❌ Error saving prediction: {str(e)}")
            return False

    def _update_patient_predictions(self, patient_id: str, prediction_data: Dict[str, Any]):
        """Update patient's prediction history"""
        try:
            patient_ref = self.db.collection('patients').document(patient_id)
            patient_doc = patient_ref.get()

            if patient_doc.exists:
                patient_data = patient_doc.to_dict()
                predictions = patient_data.get('predictions', [])
                predictions.append(prediction_data)

                # Keep only last 50 predictions
                if len(predictions) > 50:
                    predictions = predictions[-50:]

                patient_ref.update({'predictions': predictions})
        except Exception as e:
            print(f"❌ Error updating patient predictions: {str(e)}")

    def get_patient_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get patient data by email"""
        if self.demo_mode:
            return {
                "patient_id": f"P{hash(email) % 10000:04d}",
                "name": email.split('@')[0],
                "email": email,
                "predictions": [],
                "created_at": datetime.utcnow().isoformat()
            }

        try:
            # First get user to find patient_id
            user = self.get_user(email)
            if not user or user.get('role') != 'patient':
                return None

            patient_id = user.get('patient_id')
            if not patient_id:
                return None

            patient_ref = self.db.collection('patients').document(patient_id)
            patient_doc = patient_ref.get()

            if patient_doc.exists:
                return patient_doc.to_dict()
            return None
        except Exception as e:
            print(f"❌ Error getting patient: {str(e)}")
            return None

    def get_patient_predictions(self, patient_id: str) -> List[Dict[str, Any]]:
        """Get predictions for a specific patient"""
        if self.demo_mode:
            return []

        try:
            patient_ref = self.db.collection('patients').document(patient_id)
            patient_doc = patient_ref.get()

            if patient_doc.exists:
                patient_data = patient_doc.to_dict()
                return patient_data.get('predictions', [])
            return []
        except Exception as e:
            print(f"❌ Error getting patient predictions: {str(e)}")
            return []

    def save_contact_message(self, message_data: Dict[str, Any]) -> bool:
        """Save contact message"""
        if self.demo_mode:
            print(f"📝 Demo: Saved contact message from {message_data['email']}")
            return True

        try:
            message_ref = self.db.collection('contact_messages').document()
            message_ref.set(message_data)
            return True
        except Exception as e:
            print(f"❌ Error saving contact message: {str(e)}")
            return False

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        if self.demo_mode:
            return {
                "total_patients": 12,
                "total_predictions": 45,
                "detection_rate": 87.0,
                "avg_confidence": 89.0
            }

        try:
            # Get total patients
            patients_query = self.db.collection('patients').count()
            total_patients = patients_query.get()[0][0]

            # Get total predictions
            predictions_query = self.db.collection('predictions').count()
            total_predictions = predictions_query.get()[0][0]

            # Calculate detection rate and avg confidence
            predictions_ref = self.db.collection('predictions')
            predictions = predictions_ref.stream()

            tumor_detected_count = 0
            total_confidence = 0
            prediction_count = 0

            for pred in predictions:
                pred_data = pred.to_dict()
                if pred_data.get('tumor_detected'):
                    tumor_detected_count += 1
                if 'confidence' in pred_data:
                    total_confidence += pred_data['confidence']
                    prediction_count += 1

            detection_rate = (tumor_detected_count / total_predictions * 100) if total_predictions > 0 else 0
            avg_confidence = (total_confidence / prediction_count * 100) if prediction_count > 0 else 0

            return {
                "total_patients": total_patients,
                "total_predictions": total_predictions,
                "detection_rate": round(detection_rate, 1),
                "avg_confidence": round(avg_confidence, 1)
            }

        except Exception as e:
            print(f"❌ Error getting dashboard stats: {str(e)}")
            return {
                "total_patients": 0,
                "total_predictions": 0,
                "detection_rate": 0,
                "avg_confidence": 0
            }
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
