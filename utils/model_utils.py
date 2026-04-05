"""
Model utilities for loading and making predictions
"""

import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any
import tensorflow as tf
from PIL import Image
import io

class ModelUtils:
    """Utility class for model operations"""
    
    # Confidence thresholds for tumor detection
    CONFIDENCE_THRESHOLD = 0.7
    
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
        }
    }
    
    @staticmethod
    def load_model(model_path: str):
        """
        Load pre-trained model
        
        Args:
            model_path: Path to model file
        
        Returns:
            Loaded model
        """
        try:
            model = tf.keras.models.load_model(model_path)
            print(f"✅ Model loaded successfully from {model_path}")
            return model
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            return None
    
    @staticmethod
    def predict_tumor(model, image_data, confidence_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Make prediction on image
        
        Args:
            model: Loaded model
            image_data: Image file (PIL Image or bytes)
            confidence_threshold: Threshold for positive prediction
        
        Returns:
            Dictionary with prediction results
        """
        try:
            # Convert image data to PIL Image if needed
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data
            
            # Preprocess image
            image = image.convert('RGB')
            image = image.resize((224, 224))
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            
            # Make prediction
            prediction = model.predict(image_array, verbose=0)
            tumor_probability = float(prediction[0][0])
            
            # Determine if tumor detected
            tumor_detected = tumor_probability >= confidence_threshold
            confidence = max(tumor_probability, 1 - tumor_probability)
            
            result = {
                'tumor_probability': tumor_probability,
                'tumor_detected': tumor_detected,
                'confidence': confidence,
                'class': 'Tumor Detected' if tumor_detected else 'No Tumor',
                'threshold_used': confidence_threshold
            }
            
            return result
        
        except Exception as e:
            print(f"❌ Error making prediction: {str(e)}")
            return {
                'error': str(e),
                'tumor_detected': None,
                'confidence': 0.0
            }
    
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
