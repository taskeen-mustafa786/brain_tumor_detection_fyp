"""
FastAPI Backend for Brain Tumor Detection System
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
import uvicorn
import os
from datetime import datetime, timedelta
import jwt
import re
from pathlib import Path

# Import our utilities
import sys
sys.path.append('..')
from utils.model_utils import ModelUtils
from utils.firestore_config import FirestoreDB
from utils.patient_db import PatientDatabase

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="Brain Tumor Detection API",
    description="FastAPI backend for brain tumor detection with Firebase authentication",
    version="1.0.0"
)

# CORS middleware
BACKEND_HOST = os.getenv("HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("PORT", 8001))
ALLOWED_ORIGINS = os.getenv(
    "ALLOW_ORIGINS",
    "http://localhost:8000,http://localhost:8080,http://localhost:3000,http://localhost:8501"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret_here")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Password validation regex
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

FIREBASE_PUBLIC_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}

# Pydantic Models
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    @validator('password')
    def validate_password(cls, v):
        if not re.match(PASSWORD_REGEX, v):
            raise ValueError(
                'Password must be at least 8 characters long and contain: '
                '1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character'
            )
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class PatientCreate(BaseModel):
    name: str
    patient_id: str
    age: int
    gender: str
    blood_type: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
    medications: Optional[str] = None
    allergies: Optional[str] = None

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

# Global variables
model = None
firestore_db = None
patient_db = None

# Initialize services
def init_services():
    global model, firestore_db, patient_db

    # Validate JWT Secret
    if JWT_SECRET == "your_jwt_secret_here":
        print("⚠️ WARNING: JWT_SECRET is using default value. Update .env file for production!")
    else:
        print("✅ JWT_SECRET configured from environment")

    # Initialize model
    model_path = os.getenv("MODEL_PATH", "TL-Model/TL_btd_model.h5")
    if os.path.exists(model_path):
        model = ModelUtils.load_model(model_path)
    else:
        print("⚠️ Model file not found, using demo mode")
        model = "DEMO_MODEL"

    # Initialize Firestore
    try:
        firestore_db = FirestoreDB()
        print("✅ Firestore initialized")
    except Exception as e:
        print(f"❌ Firestore initialization failed: {e}")
        firestore_db = None

    # Initialize Patient Database
    if firestore_db:
        try:
            patient_db = PatientDatabase(firestore_db)
            print("✅ Patient database initialized")
        except Exception as e:
            print(f"❌ Patient database initialization failed: {e}")
            patient_db = None
    else:
        patient_db = None

# Authentication functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user_role(email: str = Depends(verify_token)) -> Dict[str, Any]:
    """Get current user with role information"""
    if not firestore_db:
        # Demo mode - return mock user
        return {
            "email": email,
            "name": email.split('@')[0],
            "role": "patient",  # Default role
            "patient_id": f"P{hash(email) % 10000:04d}"
        }

    try:
        user_data = firestore_db.get_user(email)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Routes
@app.on_event("startup")
async def startup_event():
    init_services()

@app.get("/")
async def root():
    return {"message": "Brain Tumor Detection API", "status": "running"}

@app.get("/config")
async def get_config():
    """Return public Firebase configuration for frontend initialization."""
    public_config = {k: v for k, v in FIREBASE_PUBLIC_CONFIG.items() if v}
    return {
        "firebase": public_config,
        "auth": {
            "jwt_secret_configured": JWT_SECRET != "your_jwt_secret_here"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint with service status"""
    return {
        "status": "healthy",
        "services": {
            "firebase_configured": bool(FIREBASE_PUBLIC_CONFIG.get("apiKey")),
            "firestore_connected": firestore_db is not None and not firestore_db.demo_mode if firestore_db else False,
            "firestore_demo_mode": firestore_db.demo_mode if firestore_db else True,
            "model_loaded": model != "DEMO_MODEL",
            "jwt_secret_configured": JWT_SECRET != "your_jwt_secret_here"
        },
        "environment": {
            "app_env": os.getenv("APP_ENV", "development"),
            "debug": os.getenv("DEBUG", "false").lower() == "true"
        }
    }

@app.post("/auth/register")
async def register(user: UserRegister):
    """Register a new user"""
    if not firestore_db:
        # Demo mode
        return {
            "message": "User registered successfully (demo mode)",
            "email": user.email,
            "name": user.name
        }

    try:
        # Check if user already exists
        existing_user = firestore_db.get_user(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create user
        user_data = {
            "email": user.email,
            "name": user.name,
            "role": "patient",  # Default role
            "created_at": datetime.utcnow().isoformat(),
            "patient_id": f"P{hash(user.email) % 10000:04d}"
        }

        success = firestore_db.create_user(user_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create user")

        return {"message": "User registered successfully", "user": user_data}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/auth/login")
async def login(user: UserLogin):
    """Authenticate user and return JWT token"""
    if not firestore_db:
        # Demo mode - accept any email/password
        if len(user.password) >= 8:  # Basic check
            access_token = create_access_token(data={"sub": user.email})
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "email": user.email,
                    "name": user.email.split('@')[0],
                    "role": "patient",
                    "patient_id": f"P{hash(user.email) % 10000:04d}"
                }
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    try:
        # Verify user credentials
        user_data = firestore_db.authenticate_user(user.email, user.password)
        if not user_data:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create access token
        access_token = create_access_token(data={"sub": user.email})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.get("/auth/me")
async def get_current_user(current_user: Dict[str, Any] = Depends(get_current_user_role)):
    """Get current user information"""
    return current_user

@app.post("/predict")
async def predict_tumor(
    file: UploadFile = File(...),
    scan_type: str = "MRI",
    current_user: Dict[str, Any] = Depends(get_current_user_role)
):
    """Make tumor prediction on uploaded image"""
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read image data
        image_data = await file.read()

        # Make prediction
        result = ModelUtils.predict_tumor(model, image_data)

        # Add metadata
        result.update({
            "scan_type": scan_type,
            "timestamp": datetime.utcnow().isoformat(),
            "user_email": current_user["email"],
            "patient_id": current_user.get("patient_id")
        })

        # Save prediction to database
        if firestore_db:
            try:
                firestore_db.save_prediction(result)
            except Exception as e:
                print(f"Warning: Failed to save prediction: {e}")

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/patients/me")
async def get_my_patient_data(current_user: Dict[str, Any] = Depends(get_current_user_role)):
    """Get current user's patient data"""
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Access denied")

    if not firestore_db:
        # Demo data
        return {
            "patient_id": current_user.get("patient_id", "P0001"),
            "name": current_user["name"],
            "email": current_user["email"],
            "predictions": [],
            "created_at": datetime.utcnow().isoformat()
        }

    try:
        patient_data = firestore_db.get_patient_by_email(current_user["email"])
        if not patient_data:
            raise HTTPException(status_code=404, detail="Patient data not found")

        return patient_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get patient data: {str(e)}")

@app.get("/patients/{patient_id}/predictions")
async def get_patient_predictions(
    patient_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user_role)
):
    """Get predictions for a specific patient (only own data)"""
    if current_user["role"] != "patient" or current_user.get("patient_id") != patient_id:
        raise HTTPException(status_code=403, detail="Access denied")

    if not firestore_db:
        # Demo data
        return []

    try:
        predictions = firestore_db.get_patient_predictions(patient_id)
        return predictions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get predictions: {str(e)}")

@app.post("/contact")
async def send_contact_message(message: ContactMessage):
    """Send contact message/suggestion"""
    if not firestore_db:
        # Demo mode
        return {"message": "Message sent successfully (demo mode)"}

    try:
        message_data = {
            **message.dict(),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "unread"
        }

        success = firestore_db.save_contact_message(message_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send message")

        return {"message": "Message sent successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@app.get("/dashboard/stats")
async def get_dashboard_stats(current_user: Dict[str, Any] = Depends(get_current_user_role)):
    """Get dashboard statistics"""
    if not firestore_db:
        # Demo stats
        return {
            "total_patients": 12,
            "total_predictions": 45,
            "detection_rate": 87.0,
            "avg_confidence": 89.0,
            "model_performance": ModelUtils.get_test_results()
        }

    try:
        stats = firestore_db.get_dashboard_stats()
        stats["model_performance"] = ModelUtils.get_test_results()
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")

@app.get("/model/info")
async def get_model_info():
    """Get model information and performance metrics"""
    return {
        "models": ModelUtils.get_test_results(),
        "tumor_types": ModelUtils.TUMOR_TYPES,
        "supported_features": ["tumor_detection", "tumor_classification", "confidence_scoring"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)