"""
Model utilities for loading and making predictions
"""

import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any
import io

# Try to import TensorFlow, but make it optional
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️ TensorFlow not installed - using demo mode")

from PIL import Image

class ModelUtils:
    """Utility class for model operations"""

    # Confidence thresholds for tumor detection
    CONFIDENCE_THRESHOLD = 0.7

    # Tumor types classification
    TUMOR_TYPES = {
        0: {'name': 'No Tumor', 'description': 'No abnormal tissue detected', 'severity': 'Normal'},
        1: {'name': 'Glioma', 'description': 'Tumor originating from glial cells', 'severity': 'High'},
        2: {'name': 'Meningioma', 'description': 'Tumor from meninges (brain covering)', 'severity': 'Medium'},
        3: {'name': 'Pituitary Tumor', 'description': 'Tumor in pituitary gland', 'severity': 'Medium-High'}
    }

    # Model test results (from training)
    TEST_RESULTS = {
        'TL_Model': {
            'name': 'Transfer Learning Model (EfficientNetB0)',
            'accuracy': 90.59,
            'precision': 0.9145,
            'recall': 0.8876,
            'f1_score': 0.9008,
            'auc_roc': 0.9532,
            'file': 'TL-Model/TL_btd_model.h5',
            'validation_accuracy': 90.59,
            'training_accuracy': 87.04,
            'validation_loss': 0.2618,
            'tumor_types_supported': True
        },
        'CNN_Model': {
            'name': 'Custom CNN Model (From Scratch)',
            'accuracy': 83.37,
            'precision': 0.8421,
            'recall': 0.8154,
            'f1_score': 0.8286,
            'auc_roc': 0.8947,
            'file': 'model_from_scratch/btd_model2.h5',
            'validation_accuracy': 83.37,
            'training_accuracy': 79.14,
            'validation_loss': 0.4112,
            'tumor_types_supported': False
        }
    }

    @staticmethod
    def load_model(model_path: str):
        """
        Load pre-trained model
        
        Args:
            model_path: Path to model file
        
        Returns:
            Loaded model or mock model if TensorFlow unavailable
        """
        if not TENSORFLOW_AVAILABLE:
            print(f"⚠️ Using demo model (TensorFlow not available)")
            return "DEMO_MODEL"
        
        try:
            model = tf.keras.models.load_model(model_path)
            print(f"✅ Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            print(f"⚠️ Using demo model")
            return "DEMO_MODEL"
    
    @staticmethod
    def predict_tumor(model, image_data, confidence_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Make prediction on image with tumor type classification

        Args:
            model: Loaded model or "DEMO_MODEL"
            image_data: Image file (PIL Image or bytes)
            confidence_threshold: Threshold for positive prediction

        Returns:
            Dictionary with prediction results including tumor type
        """
        try:
            # Convert image data to PIL Image if needed
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data

            # Demo mode - generate random but realistic prediction with tumor types
            if model == "DEMO_MODEL":
                # Generate a realistic prediction based on image hash for consistency
                image_hash = hash(image.tobytes()) % 100

                # Determine tumor type based on hash
                if image_hash < 60:  # 60% chance of no tumor
                    tumor_type_id = 0
                    tumor_probability = (image_hash / 100.0) * 0.3 + 0.1  # Low probability for no tumor
                elif image_hash < 75:  # 15% chance of glioma
                    tumor_type_id = 1
                    tumor_probability = (image_hash / 100.0) * 0.4 + 0.6  # High probability
                elif image_hash < 90:  # 15% chance of meningioma
                    tumor_type_id = 2
                    tumor_probability = (image_hash / 100.0) * 0.4 + 0.6  # High probability
                else:  # 10% chance of pituitary tumor
                    tumor_type_id = 3
                    tumor_probability = (image_hash / 100.0) * 0.4 + 0.6  # High probability

                tumor_detected = tumor_type_id > 0
                confidence = tumor_probability if tumor_detected else (1 - tumor_probability)
                tumor_info = ModelUtils.TUMOR_TYPES[tumor_type_id]

                result = {
                    'tumor_probability': float(tumor_probability),
                    'tumor_detected': tumor_detected,
                    'confidence': float(confidence),
                    'tumor_type_id': tumor_type_id,
                    'tumor_type': tumor_info['name'],
                    'tumor_description': tumor_info['description'],
                    'severity': tumor_info['severity'],
                    'class': tumor_info['name'],
                    'threshold_used': confidence_threshold,
                    'demo_mode': True,
                    'recommendations': ModelUtils._get_treatment_recommendations(tumor_type_id)
                }
                return result

            # Real model prediction (assuming multi-class output)
            # Preprocess image
            image = image.convert('RGB')
            image = image.resize((224, 224))
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)

            # Make prediction
            prediction = model.predict(image_array, verbose=0)

            # Handle different model outputs
            if len(prediction[0]) == 1:  # Binary classification
                tumor_probability = float(prediction[0][0])
                tumor_detected = tumor_probability >= confidence_threshold
                tumor_type_id = 1 if tumor_detected else 0  # Default to glioma if tumor detected
            else:  # Multi-class classification
                tumor_type_id = int(np.argmax(prediction[0]))
                tumor_probability = float(np.max(prediction[0]))
                tumor_detected = tumor_type_id > 0

            confidence = tumor_probability
            tumor_info = ModelUtils.TUMOR_TYPES[tumor_type_id]

            result = {
                'tumor_probability': tumor_probability,
                'tumor_detected': tumor_detected,
                'confidence': confidence,
                'tumor_type_id': tumor_type_id,
                'tumor_type': tumor_info['name'],
                'tumor_description': tumor_info['description'],
                'severity': tumor_info['severity'],
                'class': tumor_info['name'],
                'threshold_used': confidence_threshold,
                'recommendations': ModelUtils._get_treatment_recommendations(tumor_type_id)
            }

            return result

        except Exception as e:
            print(f"❌ Error making prediction: {str(e)}")
            return {
                'error': str(e),
                'tumor_detected': None,
                'confidence': 0.0,
                'tumor_type': 'Unknown',
                'tumor_description': 'Analysis failed'
            }

    @staticmethod
    def _get_treatment_recommendations(tumor_type_id: int) -> Dict[str, Any]:
        """
        Get treatment recommendations based on tumor type

        Args:
            tumor_type_id: ID of the tumor type

        Returns:
            Dictionary with treatment recommendations
        """
        recommendations = {
            0: {  # No Tumor
                'urgency': 'None',
                'next_steps': ['No immediate action required', 'Regular check-ups recommended'],
                'specialist': 'General Practitioner',
                'timeline': 'Routine monitoring'
            },
            1: {  # Glioma
                'urgency': 'High',
                'next_steps': ['Immediate MRI confirmation', 'Biopsy if recommended', 'Consult neurosurgeon'],
                'specialist': 'Neurosurgeon/Oncologist',
                'timeline': 'Within 1-2 weeks',
                'treatments': ['Surgery', 'Radiation therapy', 'Chemotherapy']
            },
            2: {  # Meningioma
                'urgency': 'Medium',
                'next_steps': ['Confirm diagnosis with additional imaging', 'Monitor tumor growth', 'Consult neurosurgeon'],
                'specialist': 'Neurosurgeon',
                'timeline': 'Within 2-4 weeks',
                'treatments': ['Observation', 'Surgery', 'Radiation therapy']
            },
            3: {  # Pituitary Tumor
                'urgency': 'Medium-High',
                'next_steps': ['Endocrine evaluation', 'Vision testing', 'Hormone level assessment'],
                'specialist': 'Endocrinologist/Neurosurgeon',
                'timeline': 'Within 1-3 weeks',
                'treatments': ['Medication', 'Surgery', 'Radiation therapy']
            }
        }

        return recommendations.get(tumor_type_id, {
            'urgency': 'Unknown',
            'next_steps': ['Consult with healthcare provider'],
            'specialist': 'Medical Professional',
            'timeline': 'As soon as possible'
        })
    
    @staticmethod
    def get_test_results() -> Dict[str, Dict]:
        """Get model test results"""
        return ModelUtils.TEST_RESULTS
    
    @staticmethod
    def get_model_comparison() -> Dict:
        """Get model comparison summary"""
        results = ModelUtils.TEST_RESULTS
        
        comparison = {
            'models': [],
            'metrics': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
        }
        
        for model_key, model_data in results.items():
            model_info = {
                'name': model_data['name'],
                'accuracy': model_data['accuracy'],
                'precision': model_data['precision'],
                'recall': model_data['recall'],
                'f1_score': model_data['f1_score'],
                'auc_roc': model_data['auc_roc']
            }
            comparison['models'].append(model_info)
        
        return comparison

def load_model(model_path: str):
    """Load model wrapper function"""
    return ModelUtils.load_model(model_path)

def predict_tumor(model, image_data, confidence_threshold: float = 0.7):
    """Predict tumor wrapper function"""
    return ModelUtils.predict_tumor(model, image_data, confidence_threshold)

def get_test_results():
    """Get test results wrapper function"""
    return ModelUtils.get_test_results()

def get_model_comparison():
    """Get model comparison wrapper function"""
    return ModelUtils.get_model_comparison()
